"""Re-adjudicate items whose first-pass adjudication returned empty.

Crash-resilient version: every single adjudication is persisted to
coding/auto/adjudications.jsonl the moment it returns, runs are resumable,
and the merge into final_coded.csv is (re)applied on every invocation -
so repeated short foreground runs converge even if a run is killed.
4 worker threads; MiniMax-M3 with M2.7 fallback, 30k token budget.
"""

import io
import json
import queue
import re
import sys
import threading
import time
from pathlib import Path

import pandas as pd
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
AUTO = ROOT / "coding" / "auto"
ITEMS = ROOT / "coding" / "items"
SIDE = AUTO / "adjudications.jsonl"
CLASSES = ["CD", "CV", "CN", "VZ"]
SLUGS = ["minimax/minimax-m3", "minimax/minimax-m2.7"]

api_key = re.search(r"sk-or-[\w-]+",
                    Path(r"D:\onedrive\桌面\论文\可计算课堂\api.txt").read_text(
                        encoding="utf-8")).group(0)
lock = threading.Lock()


def adjudicate(bid, q_cls, l_cls):
    item = (ITEMS / f"{bid}.txt").read_text(encoding="utf-8")[:6000]
    prompt = (
        "你是金融学错误分类的仲裁人。两位编码员对下面这条AI生成代码的失败记录"
        "给出了不同分类。类别定义：CD=纯编程错误；CV=模型正确但用了错误的、"
        "有教科书地位的惯例（年化天数/复利/单位/符号/ddof/vega报价等）；"
        "CN=概念或公式本身用错（含硬编码四舍五入常数）；VZ=数对图错。"
        "机械判据：换惯例重算能变对且该惯例有教科书地位→CV，否则CN。\n\n"
        f"编码员1判 {q_cls}\n编码员2判 {l_cls}\n\n"
        f"=== 记录 ===\n{item}\n\n"
        '只输出JSON：{"primary_class":"CD|CV|CN|VZ"}')
    for slug in SLUGS:
        for _ in range(2):
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json={"model": slug, "max_tokens": 30000,
                          "messages": [{"role": "user", "content": prompt}]},
                    timeout=240, headers={"Authorization": f"Bearer {api_key}"})
                r.raise_for_status()
                text = r.json()["choices"][0]["message"]["content"] or ""
                m = re.search(r"\{.*?\}", text, re.S)
                if m:
                    d = json.loads(m.group(0))
                    if d.get("primary_class") in CLASSES:
                        return d["primary_class"], slug
            except (requests.RequestException, json.JSONDecodeError):
                pass
            time.sleep(2)
    return None, None


def main():
    df = pd.read_csv(AUTO / "final_coded.csv")
    done = {}
    if SIDE.exists():
        for line in SIDE.read_text(encoding="utf-8").splitlines():
            try:
                d = json.loads(line)
                done[d["blind_id"]] = d
            except json.JSONDecodeError:
                pass

    todo = df[(df.source == "fallback_Q") & (~df.blind_id.isin(done))]
    print(f"pending adjudications: {len(todo)} (already persisted: {len(done)})",
          flush=True)

    jobq = queue.Queue()
    for _, row in todo.iterrows():
        jobq.put((row.blind_id, row.coder_Q, row.coder_K))

    def worker():
        while True:
            try:
                bid, qc, lc = jobq.get_nowait()
            except queue.Empty:
                return
            cls, slug = adjudicate(bid, qc, lc)
            with lock:
                if cls:
                    with open(SIDE, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"blind_id": bid, "class": cls,
                                            "slug": slug}) + "\n")
                    print(f"  {bid} -> {cls} ({slug.split('/')[1]})", flush=True)
                else:
                    print(f"  {bid} -> FAILED both slugs", flush=True)

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # merge everything persisted so far
    done = {}
    if SIDE.exists():
        for line in SIDE.read_text(encoding="utf-8").splitlines():
            try:
                d = json.loads(line)
                done[d["blind_id"]] = d
            except json.JSONDecodeError:
                pass
    n_applied = 0
    for idx, row in df[df.source == "fallback_Q"].iterrows():
        if row.blind_id in done:
            df.loc[idx, "final_class"] = done[row.blind_id]["class"]
            df.loc[idx, "source"] = \
                f"adjudicated:{done[row.blind_id]['slug'].split('/')[1]}"
            n_applied += 1
    df.to_csv(AUTO / "final_coded.csv", index=False, encoding="utf-8-sig")
    remaining = (df.source == "fallback_Q").sum()
    print(f"applied {n_applied}; remaining fallback: {remaining}", flush=True)

    # regenerate fig2 data
    res = pd.read_csv(ROOT / "runs" / "results_formal.csv")
    cd_auto = res[(res.condition == "C1") & (res.bucket == "code_error")]
    fig2 = df[df.condition == "C1"][["model", "final_class", "hardcoded", "declared"]]
    fig2 = pd.concat([fig2, pd.DataFrame(
        {"model": cd_auto.model, "final_class": "CD", "hardcoded": 0,
         "declared": "N"})], ignore_index=True)
    fig2.to_csv(AUTO / "fig2_data.csv", index=False, encoding="utf-8-sig")
    n = len(fig2)
    print(f"Fig2 N={n}: " + ", ".join(
        f"{c} {int((fig2.final_class==c).sum())} "
        f"({100*(fig2.final_class==c).mean():.1f}%)" for c in CLASSES), flush=True)


if __name__ == "__main__":
    main()

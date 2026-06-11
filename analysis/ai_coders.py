"""Heterogeneous AI double-coding of all failure items.

Two LLM coders - architecturally distinct from each other AND from the
three evaluated models - independently assign the codebook classes to all
686 items, blinded to condition/model (they see the same item files the
human packet uses). Disclosed in the paper as AI coders (DEVIATIONS #7).

Coders:  qwen/qwen3-235b-a22b-2507  (coder Q)
         moonshotai/kimi-k2.6       (coder K)
Adjudicator for Q/K disagreements unresolved by the mechanical layer:
         meta-llama/llama-4-maverick (run later in finalize step)

Resume-safe: one jsonl per coder keyed by blind_id.
Usage: python ai_coders.py --key-file <path> [--workers 8] [--max-items N]
"""

import argparse
import json
import queue
import re
import sys
import threading
import time
from pathlib import Path

import pandas as pd
import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = yaml.safe_load((ROOT / "config" / "models.yaml").read_text(encoding="utf-8"))
ITEMS = ROOT / "coding" / "items"
KEY = ROOT / "coding" / "_key_do_not_open.csv"
OUTDIR = ROOT / "coding" / "auto"

# Coder K (Kimi K2.6) proved unstable in production (very slow thinking,
# intermittent empty completions, silent process crashes); replaced by
# Llama-4-Maverick as coder L before any reconciliation was run. Kimi's
# 197 completed votes are archived as supplementary third votes
# (ai_coder_K.jsonl). Disclosed in DEVIATIONS #7.
CODERS = {"Q": "qwen/qwen3-235b-a22b-2507", "L": "meta-llama/llama-4-maverick"}

MANUAL = """你是一名金融学课程的研究助理，负责给"AI生成的金融计算代码的失败记录"做错误分类。
严格按以下手册判断，输出JSON。

【四个类别】
CD=代码病：纯编程错误（变量接错、库误用导致错误数值）。
CV=约定病：模型与公式正确，但采用了错误的、却在教科书/市场实务中真实存在的惯例。
  惯例清单：年化天数252/250/365；离散vs连续复利；付息频率年付vs半年付；百分比vs小数；
  VaR正负号；ddof=0vs1；年利率/12vs几何折算；vega每单位vs每百分点；凸性少除(1+y)²；
  60/40权重对应顺序；久期一阶vs加凸性vs精确重定价；历史VaR分位数插值方式；金额单位(元vs万元)。
CN=概念病：模型/公式/定义本身用错，任何惯例替换都救不回来。
  典型：麦考利久期填进修正久期；相关阵当协方差阵；单尾95%VaR用1.96(双尾值)；CAPM公式写错。
VZ=图形病：要求的数值全对但图缺失/错误。

【机械判据】把它实际用的选择代回去重算：变对且该选择有教科书地位→CV；否则→CN。
【特别规则13】代码不做计算、直接硬编码一个四舍五入过的常数（提交值与参考值差<0.2%）
→ 判 CN，convention 字段填 "hardcoded_constant"。
【易错判例】单尾95%用1.96→CN（"双尾VaR"无教科书地位）；声明用A惯例但代码实现B→CV
且 declared=N；忽略题目给定的无风险利率(算毛夏普)→CV。

【declared 判断】只看注释/文字说明/result里的字符串是否说明了所用惯例；
代码里出现 sqrt(365) 这类数字本身不算声明。

只输出一个JSON对象，不要其他文字：
{"primary_class":"CD|CV|CN|VZ","convention":"若CV/规则13填所用惯例，否则空串",
"declared":"Y|N","rationale":"不超过30字"}"""


def call(slug, prompt, api_key):
    url = CONFIG["api"]["base_url"].rstrip("/") + "/chat/completions"
    body = {"model": slug, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 16384}
    for attempt in range(4):
        try:
            resp = requests.post(url, json=body, timeout=300,
                                 headers={"Authorization": f"Bearer {api_key}"})
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep([5, 15, 60, 60][attempt])
                continue
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"] or ""
        except requests.RequestException:
            time.sleep([5, 15, 60, 60][attempt])
    raise RuntimeError("api failed")


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if d.get("primary_class") not in ("CD", "CV", "CN", "VZ"):
        return None
    d["declared"] = "Y" if str(d.get("declared", "N")).upper().startswith("Y") else "N"
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--max-items", type=int, default=0)
    args = ap.parse_args()
    api_key = re.search(r"sk-or-[\w-]+",
                        Path(args.key_file).read_text(encoding="utf-8")).group(0)
    OUTDIR.mkdir(parents=True, exist_ok=True)

    blind_ids = sorted(p.stem for p in ITEMS.glob("B*.txt"))
    if args.max_items:
        blind_ids = blind_ids[:args.max_items]

    jobs = []
    for coder, slug in CODERS.items():
        log = OUTDIR / f"ai_coder_{coder}.jsonl"
        done = set()
        if log.exists():
            for line in log.read_text(encoding="utf-8").splitlines():
                try:
                    done.add(json.loads(line)["blind_id"])
                except Exception:  # noqa: BLE001
                    pass
        jobs += [(coder, slug, b) for b in blind_ids if b not in done]

    print(f"to code: {len(jobs)} (coders x items, resume-aware)")
    q = queue.Queue()
    for j in jobs:
        q.put(j)
    lock = threading.Lock()
    counts = {"done": 0, "fail": 0}
    t0 = time.time()

    def worker():
        while True:
            try:
                coder, slug, bid = q.get_nowait()
            except queue.Empty:
                return
            item = (ITEMS / f"{bid}.txt").read_text(encoding="utf-8")[:7000]
            prompt = MANUAL + "\n\n=== 待分类记录 ===\n" + item
            try:
                text = call(slug, prompt, api_key)
                d = parse(text)
                if d is None:
                    text = call(slug, prompt + "\n\n注意：只输出JSON对象。", api_key)
                    d = parse(text)
                rec = {"blind_id": bid, "coder": coder,
                       **(d or {"primary_class": "PARSE_FAIL"}),
                       "raw": text[:400]}
            except Exception as e:  # noqa: BLE001
                rec = {"blind_id": bid, "coder": coder,
                       "primary_class": "API_FAIL", "raw": repr(e)[:200]}
            with lock:
                for retry in range(5):   # OneDrive sync can lock the file
                    try:
                        with open(OUTDIR / f"ai_coder_{coder}.jsonl", "a",
                                  encoding="utf-8") as f:
                            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        break
                    except OSError:
                        time.sleep(1 + retry)
                counts["done"] += 1
                if rec["primary_class"] in ("PARSE_FAIL", "API_FAIL"):
                    counts["fail"] += 1
                if counts["done"] % 25 == 0:
                    el = time.time() - t0
                    print(f"{counts['done']}/{len(jobs)} "
                          f"({counts['fail']} fail) {counts['done']/el*3600:.0f}/h",
                          flush=True)

    threads = [threading.Thread(target=worker, daemon=True)
               for _ in range(args.workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"FINISHED: {counts['done']} coded, {counts['fail']} parse/api failures")


if __name__ == "__main__":
    main()

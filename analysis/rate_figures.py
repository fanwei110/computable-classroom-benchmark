"""AI double-rating of T2 figure adequacy (four-item rubric, §IV.B).

Two vision-capable models, both outside the evaluated trio, independently
rate every archived figure against its task's rubric:
  R1 qwen/qwen2.5-vl-72b-instruct
  R2 meta-llama/llama-4-maverick
Adequate = all four items pass. T2 generations with no archived figure
(code never produced one) are inadequate by definition and excluded from
the rating queue. Resume-safe per rater.

Usage: python rate_figures.py --key-file <path> [--workers 6]
"""

import argparse
import base64
import json
import queue
import re
import threading
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
FIGS = ROOT / "runs" / "raw" / "formal" / "figures"
OUTDIR = ROOT / "coding" / "auto"

RATERS = {"R1": "qwen/qwen2.5-vl-72b-instruct",
          "R2": "meta-llama/llama-4-maverick"}

RUBRIC = {
    "KP1_T2": "应画出三条不同相关系数(0.15/0.45/0.75)的均值-方差前沿曲线于同一坐标系"
              "（横轴风险/波动率，纵轴期望收益），并在每条曲线上标出最小方差组合点。",
    "KP2_T2": "应画出beta从0到2的证券市场线（直线），并标出X、Y、Z三只股票的散点"
              "（坐标轴为beta与期望收益）。",
    "KP3_T2": "应画出收益率2%-9%区间的债券精确价格曲线，并叠加基于久期的近似"
              "（直线或二次曲线），图例区分精确与近似。",
    "KP4_T2": "应画出标的价70-140区间的看涨期权delta曲线，三个波动率(15%/27.6%/40%)"
              "各一条，图例区分（delta范围0到1）。",
    "KP5_T2": "应画出日损益分布直方图，并用竖线标出95%一日VaR位置（最好有标注）。",
    "KP6_T2": "应画出60日滚动年化夏普比率的时间序列曲线。",
}

PROMPT = """你是图表质量评审。下面是一张AI生成的金融教学图，本应满足：
{rubric}

按四项二元评分（是=Y，否=N）：
item1 要求的曲线/对象齐全（数量与类型对）
item2 坐标轴含义正确（即使无标签，量纲取值范围合理也算Y；明显画错轴为N）
item3 多对象时有图例或可区分标注（单对象图自动Y）
item4 整体不误导（形状/方向/位置无明显错误）

只输出JSON：{{"item1":"Y|N","item2":"Y|N","item3":"Y|N","item4":"Y|N"}}"""


def call(slug, prompt, img_b64, mime, api_key):
    body = {"model": slug, "max_tokens": 8192,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:{mime};base64,{img_b64}"}}]}]}
    for attempt in range(3):
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                              json=body, timeout=300,
                              headers={"Authorization": f"Bearer {api_key}"})
            if r.status_code in (429, 500, 502, 503):
                time.sleep([5, 15, 60][attempt])
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"] or ""
        except requests.RequestException:
            time.sleep([5, 15, 60][attempt])
    raise RuntimeError("api failed")


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    items = {k: str(d.get(k, "N")).upper().startswith("Y")
             for k in ("item1", "item2", "item3", "item4")}
    items["adequate"] = all(items.values())
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    api_key = re.search(r"sk-or-[\w-]+",
                        Path(args.key_file).read_text(encoding="utf-8")).group(0)
    OUTDIR.mkdir(parents=True, exist_ok=True)

    figs = sorted(p for p in FIGS.glob("*") if p.suffix.lower()
                  in (".png", ".jpg", ".jpeg", ".pdf") and not p.name.startswith("_"))
    figs = [p for p in figs if p.suffix.lower() != ".pdf"]  # vision needs raster
    jobs = []
    for rater in RATERS:
        log = OUTDIR / f"fig_rater_{rater}.jsonl"
        done = set()
        if log.exists():
            for line in log.read_text(encoding="utf-8").splitlines():
                try:
                    done.add(json.loads(line)["run_id"])
                except Exception:  # noqa: BLE001
                    pass
        jobs += [(rater, p) for p in figs if p.stem not in done]
    print(f"figures: {len(figs)}; rating jobs to run: {len(jobs)}")

    q = queue.Queue()
    for j in jobs:
        q.put(j)
    lock = threading.Lock()
    counts = {"done": 0, "fail": 0}
    t0 = time.time()

    def worker():
        while True:
            try:
                rater, p = q.get_nowait()
            except queue.Empty:
                return
            run_id = p.stem
            task_id = re.search(r"KP\d_T2", run_id).group(0)
            mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
            b64 = base64.b64encode(p.read_bytes()).decode()
            try:
                text = call(RATERS[rater], PROMPT.format(rubric=RUBRIC[task_id]),
                            b64, mime, api_key)
                d = parse(text)
                rec = {"run_id": run_id, "rater": rater,
                       **(d or {"adequate": None, "parse_fail": True}),
                       "raw": text[:200]}
            except Exception as e:  # noqa: BLE001
                rec = {"run_id": run_id, "rater": rater, "adequate": None,
                       "api_fail": True, "raw": repr(e)[:150]}
            with lock:
                with open(OUTDIR / f"fig_rater_{rater}.jsonl", "a",
                          encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                counts["done"] += 1
                if rec.get("adequate") is None:
                    counts["fail"] += 1
                if counts["done"] % 50 == 0:
                    el = time.time() - t0
                    print(f"{counts['done']}/{len(jobs)} ({counts['fail']} fail) "
                          f"{counts['done']/el*3600:.0f}/h", flush=True)

    threads = [threading.Thread(target=worker, daemon=True)
               for _ in range(args.workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"FINISHED: {counts['done']} rated, {counts['fail']} failures")


if __name__ == "__main__":
    main()

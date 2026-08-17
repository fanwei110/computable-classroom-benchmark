"""Phase-C robustness experiments (revision R&R), run on the standalone
DeepSeek API (deepseek-chat) to keep cost low. Reuses the FROZEN judge and the
frozen C1/C4 prompt material; adds nothing to the preregistered pipeline.

Two experiments (a representative subset of 6 tasks, one per knowledge point):
  ablation    — decompose the C4 template into components by leave-one-out /
                minimal variants, to unbundle the "structure" factor
                (rebuts: is the +29.6pp structure effect scaffold or task-reg?).
                variants: C1(raw) | contract_only | minus_scaffold |
                          minus_convention | C4_full
  temperature — C1 & C4_full at T in {0.0, 0.5, 1.0}
                (rebuts: were provider-default results a lucky temperature?).

Key handling: DEEPSEEK_API_KEY from the environment ONLY; never logged/written.
Model described honestly as "DeepSeek (deepseek-chat)", a representative
deployed model — NOT identical to the main study's M2 (deepseek-v4-pro).
Resume-safe: existing run_ids in runs/exp_results.csv are skipped.

Usage:
  export DEEPSEEK_API_KEY=sk-...
  python exp_runner.py --exp both [--reps 5] [--max 0] [--model deepseek-chat]
"""
import argparse, csv, hashlib, json, os, sys, time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from runner import extract_code, output_contract_zh, load_task  # noqa: E402
sys.path.insert(0, str(ROOT / "harness"))
from judge import judge  # noqa: E402

TASKS = ["KP1_T1", "KP2_T3", "KP3_T1", "KP4_T1", "KP5_T3", "KP6_T1"]
ABL_VARIANTS = ["C1", "contract_only", "minus_scaffold", "minus_convention", "C4_full"]
TEMPS = [0.0, 0.5, 1.0]
API_URL = "https://api.deepseek.com/chat/completions"
OUTDIR = ROOT / "runs" / "raw" / "exp"
CSV_PATH = ROOT / "runs" / "exp_results.csv"

# ---- prompt assembly (from frozen material) --------------------------------

def c4_blocks(task_id):
    """Split the frozen C4 prompt into labelled blocks (blank-line separated)."""
    text = (ROOT / "prompts" / "C4_zh" / f"{task_id}.md").read_text(encoding="utf-8")
    blocks = {}
    for para in [p.strip() for p in text.split("\n\n") if p.strip()]:
        if para.startswith("你是"):
            blocks["role"] = para
        elif para.startswith("概念"):
            blocks["concept"] = para
        elif para.startswith("课程计算约定"):
            blocks["convention"] = para
        elif para.startswith("任务"):
            blocks["task"] = para
        elif para.startswith("请按以下步骤"):
            blocks["scaffold"] = para
        elif para.startswith("写一"):
            blocks["lib"] = para
        elif para.startswith("输出契约"):
            blocks["contract"] = para
        else:
            blocks.setdefault("other", []).append(para)
    return blocks


def compose(blocks, keys):
    return "\n\n".join(blocks[k] for k in keys if k in blocks)


def ablation_prompt(task_id, variant):
    b = c4_blocks(task_id)
    order = ["role", "concept", "convention", "task", "scaffold", "lib", "contract"]
    if variant == "C1":  # raw improvised phrasing (persona A) + contract, frozen
        return (ROOT / "prompts" / "C1_final" / f"{task_id}_A.md").read_text(encoding="utf-8")
    if variant == "C4_full":
        return compose(b, order)
    if variant == "contract_only":     # task + lib + contract (no framing/scaffold/convention)
        return compose(b, ["task", "lib", "contract"])
    if variant == "minus_scaffold":    # full C4 minus the numbered steps
        return compose(b, [k for k in order if k != "scaffold"])
    if variant == "minus_convention":  # full C4 minus the convention block (~structure-only)
        return compose(b, [k for k in order if k != "convention"])
    raise ValueError(variant)


def temp_prompt(task_id, cond):
    if cond == "C1":
        return (ROOT / "prompts" / "C1_final" / f"{task_id}_A.md").read_text(encoding="utf-8")
    return compose(c4_blocks(task_id), ["role", "concept", "convention", "task",
                                        "scaffold", "lib", "contract"])

# ---- DeepSeek call ---------------------------------------------------------

def deepseek_call(model, prompt, api_key, temperature=None, max_tokens=8192):
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens}
    if temperature is not None:
        body["temperature"] = temperature
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    last = None
    for attempt in range(4):
        try:
            t0 = time.perf_counter()
            r = requests.post(API_URL, json=body, headers=headers, timeout=300)
            lat = time.perf_counter() - t0
            if r.status_code in (429, 500, 502, 503, 504):
                last = f"HTTP {r.status_code}: {r.text[:160]}"
            else:
                r.raise_for_status()
                d = r.json()
                text = d["choices"][0]["message"]["content"] or ""
                usage = d.get("usage", {})
                return text, usage, lat
        except (requests.RequestException, ValueError, KeyError) as e:
            last = repr(e)
        time.sleep([5, 15, 40][min(attempt, 2)])
    raise RuntimeError(f"deepseek API failed: {last}")

# ---- main ------------------------------------------------------------------

def load_done():
    if not CSV_PATH.exists():
        return set()
    with open(CSV_PATH, encoding="utf-8") as f:
        return {row["run_id"] for row in csv.DictReader(f)}


def jobs_for(exp, reps):
    js = []
    if exp in ("ablation", "both"):
        for t in TASKS:
            for v in ABL_VARIANTS:
                for r in range(1, reps + 1):
                    js.append(("ablation", t, v, None, r))
    if exp in ("temperature", "both"):
        for t in TASKS:
            for cond in ("C1", "C4_full"):
                for temp in TEMPS:
                    for r in range(1, reps + 1):
                        js.append(("temperature", t, cond, temp, r))
    return js


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", choices=["ablation", "temperature", "both"], default="both")
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--max", type=int, default=0, help="cap jobs (smoke test)")
    ap.add_argument("--model", default="deepseek-chat")
    args = ap.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        sys.exit("set DEEPSEEK_API_KEY in the environment")

    (OUTDIR / "code").mkdir(parents=True, exist_ok=True)
    (OUTDIR / "completions").mkdir(parents=True, exist_ok=True)
    done = load_done()
    jobs = [j for j in jobs_for(args.exp, args.reps)
            if f"{j[0]}_{j[1]}_{j[2]}_t{j[3]}_r{j[4]:02d}" not in done]
    if args.max:
        jobs = jobs[:args.max]
    print(f"to run: {len(jobs)} (already done {len(done)}), model={args.model}")

    new = not CSV_PATH.exists()
    tok_in = tok_out = 0
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["run_id", "experiment", "task_id", "variant", "temperature",
                        "rep", "exec_ok", "correct", "correct_def", "bucket", "tier",
                        "latency_api_s", "model"])
        for i, (exp, task, var, temp, rep) in enumerate(jobs, 1):
            run_id = f"{exp}_{task}_{var}_t{temp}_r{rep:02d}"
            prompt = (ablation_prompt(task, var) if exp == "ablation"
                      else temp_prompt(task, var))
            try:
                text, usage, lat = deepseek_call(args.model, prompt, api_key, temperature=temp)
            except Exception as e:  # noqa: BLE001
                print(f"[APIFAIL] {run_id}: {e}")
                continue
            tok_in += usage.get("prompt_tokens", 0)
            tok_out += usage.get("completion_tokens", 0)
            code = extract_code(text)
            cp = OUTDIR / "code" / f"{run_id}.py"
            mp = OUTDIR / "completions" / f"{run_id}.txt"
            mp.write_text(text, encoding="utf-8")
            has_code = bool(code.strip())
            if has_code:
                cp.write_text(code, encoding="utf-8")
                v = judge(task, code_path=cp, completion_path=mp)
            else:
                v = judge(task, code_path=None, completion_path=mp)
            # correctness derived exactly as analysis/aggregate_formal.py does
            bucket = v.get("bucket")
            exec_ok = int(has_code and bucket != "code_error")
            correct = int(bucket == "correct")
            correct_def = int(bucket in ("correct", "defensible"))
            w.writerow([run_id, exp, task, var, temp, rep,
                        exec_ok, correct, correct_def,
                        bucket, v.get("tier"), round(lat, 2), args.model])
            f.flush()
            cost = tok_in / 1e6 * 0.3 + tok_out / 1e6 * 1.2  # conservative $/1M
            if i % 10 == 0 or i == len(jobs):
                print(f"[{i}/{len(jobs)}] {run_id} correct={correct} "
                      f"bucket={bucket} ~${cost:.3f}")
    print(f"done. tokens in={tok_in} out={tok_out} est_cost~${tok_in/1e6*0.3+tok_out/1e6*1.2:.3f}")


if __name__ == "__main__":
    main()

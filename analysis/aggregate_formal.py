"""Aggregate the formal run: integrity check, tidy table, headline numbers.

Outputs:
  runs/results_formal.csv  - one row per generation (tidy, for stats scripts)
  prints: grid integrity; Table II numbers (exec/strict-correct by
  model x condition and pooled); Table III numbers (task type x condition,
  T3 at both tiers); task-level reliability; latency; behavior counts;
  manual-review queue size.

Strict correctness = bucket 'correct' (T3: tier strict).
Defensible-tier correctness = buckets 'correct' + 'defensible'.
Executability = code was produced AND ran without exception
(code_error and no-code completions fail it; format failures whose code ran
count as executable but not correct, per the paper's metric definitions).
"""

import io
import json
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "runs" / "raw" / "formal" / "formal.jsonl"
OUT = ROOT / "runs" / "results_formal.csv"

rows = []
for line in LOG.read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    j = r["judge"]
    bucket = j["bucket"]
    no_code = not r["code_extracted"]
    rows.append({
        "run_id": r["run_id"],
        "task_id": r["task_id"],
        "task_type": "T" + r["task_id"].split("_T")[1],
        "model": r["model"],
        "condition": r["condition"],
        "variant": r["variant"],
        "repetition": r["repetition"],
        "bucket": bucket,
        "tier": j.get("tier"),
        "behavior": j.get("behavior"),
        "needs_review": j.get("needs_review", False),
        "exec_ok": int((not no_code) and bucket != "code_error"),
        "correct": int(bucket == "correct"),
        "correct_def": int(bucket in ("correct", "defensible")),
        "latency_total_s": r["latency_s"]["total"],
        "latency_api_s": r["latency_s"]["api"],
    })

df = pd.DataFrame(rows)

# ---- integrity ------------------------------------------------------------
dup = df["run_id"].duplicated().sum()
cells = df.groupby(["model", "condition", "task_id"]).size()
bad_cells = cells[cells != 10]
print(f"INTEGRITY: n={len(df)} (expect 2160), duplicate run_ids={dup}, "
      f"cells!=10: {len(bad_cells)}")
assert len(df) == 2160 and dup == 0 and len(bad_cells) == 0

df.to_csv(OUT, index=False)
print(f"wrote {OUT.relative_to(ROOT)}\n")

pct = lambda s: f"{100*s.mean():.1f}%"  # noqa: E731

# ---- Table II: model x condition ------------------------------------------
print("=== Table II numbers: executability / strict correctness ===")
for model in ("M1", "M2", "M3", "pooled"):
    sub_m = df if model == "pooled" else df[df["model"] == model]
    parts = []
    for cond in ("C1", "C2", "C3", "C4"):
        s = sub_m[sub_m["condition"] == cond]
        parts.append(f"{cond}: {pct(s['exec_ok'])}/{pct(s['correct'])}"
                     f" ({s['correct'].sum()}/{len(s)})")
    print(f"  {model:>6s}  " + " | ".join(parts))

print("\n=== Defensible-tier correctness (pooled) ===")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[df["condition"] == cond]
    print(f"  {cond}: strict {pct(s['correct'])}  defensible {pct(s['correct_def'])}")

# ---- Table III: task type x condition (pooled) -----------------------------
print("\n=== Table III numbers: strict correctness by task type ===")
for tt in ("T1", "T2", "T3"):
    s_t = df[df["task_type"] == tt]
    parts = []
    for cond in ("C1", "C2", "C3", "C4"):
        s = s_t[s_t["condition"] == cond]
        parts.append(f"{cond}: {pct(s['correct'])} ({s['correct'].sum()}/{len(s)})")
    print(f"  {tt}  " + " | ".join(parts))
s_t3 = df[df["task_type"] == "T3"]
parts = []
for cond in ("C1", "C2", "C3", "C4"):
    s = s_t3[s_t3["condition"] == cond]
    parts.append(f"{cond}: {pct(s['correct_def'])} ({s['correct_def'].sum()}/{len(s)})")
print("  T3 (defensible tier)  " + " | ".join(parts))

# ---- task-level reliability -------------------------------------------------
print("\n=== Task-level reliability ===")
for cond in ("C1", "C4"):
    s = df[df["condition"] == cond]
    per_task_all = s.groupby("task_id")["correct"].all()
    per_tm = s.groupby(["task_id", "model"])["correct"].all()
    print(f"  {cond}: all-30-correct tasks (pooled defn): "
          f"{int(per_task_all.sum())}/18 ; "
          f"all-10-correct task-model pairs: {int(per_tm.sum())}/54")

# ---- latency ----------------------------------------------------------------
print("\n=== Latency (prompt -> executed output, s) ===")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[df["condition"] == cond]["latency_total_s"]
    print(f"  {cond}: median {s.median():.1f}  p90 {s.quantile(0.9):.1f}")
print(f"  overall p90: {df['latency_total_s'].quantile(0.9):.1f}")

# ---- behavior & review queue --------------------------------------------------
print("\n=== Behavior / queues ===")
print(f"  clarify responses: {(df['behavior']=='clarify').sum()}")
print(f"  defensible (declared alt convention): {(df['bucket']=='defensible').sum()}")
print(f"  needs_review flagged: {df['needs_review'].sum()}")
print(f"  format failures: {(df['bucket']=='format_failure').sum()} "
      f"(no-code: {((df['bucket']=='format_failure') & (df['exec_ok']==0)).sum()})")
print(f"  vis failures: {(df['bucket']=='vis_failure').sum()}")

# numeric failures by condition (error-coding denominators)
print("\n=== Coded-failure denominators (numeric_wrong + vis_failure) ===")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[df["condition"] == cond]
    n = ((s["bucket"] == "numeric_wrong") | (s["bucket"] == "vis_failure")).sum()
    print(f"  {cond}: {n}")

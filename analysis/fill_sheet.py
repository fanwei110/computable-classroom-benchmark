"""Produce the definitive fill sheet for the v3 real-data draft:
every count, percentage, delta, CI (B=10,000), and test statistic the
paper needs, written to runs/fill_sheet.txt for the data-fill edit pass.
"""

import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from bootstrap_ci import cluster_bootstrap_ci  # noqa: E402
from mixed_logit import fit_gee  # noqa: E402

df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
out = []
p = out.append


def ci_str(sub, col="correct", b=10000):
    m, lo, hi = cluster_bootstrap_ci(sub, value_col=col, b=b)
    return f"{100*m:.1f}% [{100*lo:.1f}, {100*hi:.1f}]"


p("=== pooled by condition (n=540 each) ===")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[df.condition == cond]
    p(f"{cond}: corr {s.correct.sum()}/540 = {ci_str(s)} | "
      f"def-tier {s.correct_def.sum()}/540 = {ci_str(s, 'correct_def')} | "
      f"exec {s.exec_ok.sum()}/540 = {ci_str(s, 'exec_ok')}")

p("\n=== deltas (exact fractions, pp) ===")
g = {c: df[df.condition == c].correct.sum() for c in ("C1", "C2", "C3", "C4")}
p(f"C4-C1 = {(g['C4']-g['C1'])/5.40:.1f}pp ; C2-C1 = {(g['C2']-g['C1'])/5.40:.1f}pp ; "
  f"C3-C1 = {(g['C3']-g['C1'])/5.40:.1f}pp ; C4-C2 = {(g['C4']-g['C2'])/5.40:.1f}pp ; "
  f"C4-C3 = {(g['C4']-g['C3'])/5.40:.1f}pp")

p("\n=== model x condition (n=180 cells): exec / correct with CI ===")
for m in ("M1", "M2", "M3"):
    for cond in ("C1", "C2", "C3", "C4"):
        s = df[(df.model == m) & (df.condition == cond)]
        p(f"{m} {cond}: exec {s.exec_ok.sum()}/180={100*s.exec_ok.mean():.1f}% | "
          f"corr {s.correct.sum()}/180 = {ci_str(s, b=4000)}")

p("\n=== task type x condition (n=180): strict ===")
for tt in ("T1", "T2", "T3"):
    row = []
    for cond in ("C1", "C2", "C3", "C4"):
        s = df[(df.task_type == tt) & (df.condition == cond)]
        row.append(f"{cond} {s.correct.sum()}/180={100*s.correct.mean():.1f}%")
    p(f"{tt}: " + " | ".join(row))
row = []
for cond in ("C1", "C2", "C3", "C4"):
    s = df[(df.task_type == "T3") & (df.condition == cond)]
    row.append(f"{cond} {s.correct_def.sum()}/180={100*s.correct_def.mean():.1f}%")
p("T3 defensible: " + " | ".join(row))

p("\n=== T-type gains C4-C1 (pp) ===")
for tt in ("T1", "T2", "T3"):
    a = df[(df.task_type == tt) & (df.condition == "C1")].correct.mean()
    b_ = df[(df.task_type == tt) & (df.condition == "C4")].correct.mean()
    p(f"{tt}: {100*(b_-a):.1f}pp")

p("\n=== reliability / latency / behavior ===")
for cond in ("C1", "C4"):
    s = df[df.condition == cond]
    p(f"{cond}: task-model pairs all-10 correct: "
      f"{int(s.groupby(['task_id','model']).correct.all().sum())}/54 ; "
      f"tasks all-30 correct: {int(s.groupby('task_id').correct.all().sum())}/18")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[df.condition == cond].latency_total_s
    p(f"latency {cond}: median {s.median():.1f}s p90 {s.quantile(.9):.1f}s")
p(f"latency overall: median {df.latency_total_s.median():.1f}s "
  f"p90 {df.latency_total_s.quantile(.9):.1f}s")
p(f"clarify: {(df.behavior=='clarify').sum()} of 2160")
p(f"defensible bucket total: {(df.bucket=='defensible').sum()}")
nc = df[(df.bucket == 'format_failure') & (df.exec_ok == 0)]
p("no-code by condition: " +
  ", ".join(f"{c}={len(nc[nc.condition==c])}" for c in ("C1", "C2", "C3", "C4")))
p("strict-failure totals by condition (540-correct): " +
  ", ".join(f"{c}={540-g[c]}" for c in ("C1", "C2", "C3", "C4")))

p("\n=== GEE (task clusters): correct ~ conv*struct + model ===")
fit = fit_gee(df)
for name in ("conv", "struct", "conv:struct"):
    p(f"{name}: coef={fit.params[name]:.3f} OR={np.exp(fit.params[name]):.2f} "
      f"se={fit.bse[name]:.3f} p={fit.pvalues[name]:.2e}")

text = "\n".join(out)
(ROOT / "runs" / "fill_sheet.txt").write_text(text, encoding="utf-8")
print(text)

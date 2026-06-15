"""Journal-revision statistics — single source of truth for the journal draft.

Recomputes every number the revised manuscript cites, from the raw tidy
results + final error coding, and writes runs/journal_stats.txt. Resolves
the Fig.2 population N and adds the review-requested figures:
  - mechanical lower bound per error class (immune to the kappa critique)
  - per-coder proportion intervals (Q-only vs L-only)
  - correctness conditional on executable code
  - visible vs silent failure split
  - latency truncation cost at 45 s / 60 s
  - C3-T3 vs C1-T3 bootstrap CI for the anomalous cell
Reuses bootstrap_ci.cluster_bootstrap_ci.
"""

import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from bootstrap_ci import cluster_bootstrap_ci  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
OUT = ROOT / "runs" / "journal_stats.txt"
CLASSES = ["CV", "CN", "CD", "VZ"]
lines = []


def p(s=""):
    lines.append(str(s))
    print(s)


df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
fc = pd.read_csv(ROOT / "coding" / "auto" / "final_coded.csv")

p("=" * 64)
p("JOURNAL-REVISION STATS  (source of truth for paper_C_journal)")
p("=" * 64)

# ---- 1. headline grid re-verify -------------------------------------------
p("\n[1] Headline grid (pooled, n=540/condition), strict correctness")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[df.condition == cond]
    m, lo, hi = cluster_bootstrap_ci(s, "correct", b=10000)
    e = s.exec_ok.mean()
    p(f"  {cond}: corr {s.correct.sum()}/540 = {100*m:.1f}% "
      f"[{100*lo:.1f},{100*hi:.1f}] | exec {100*e:.1f}%")
g = {c: df[df.condition == c].correct.mean() for c in ("C1", "C2", "C3", "C4")}
p(f"  deltas pp: C4-C1={100*(g['C4']-g['C1']):.1f}  C2-C1={100*(g['C2']-g['C1']):.1f}  "
  f"C3-C1={100*(g['C3']-g['C1']):.1f}  C4-C2={100*(g['C4']-g['C2']):.1f}")

# ---- 2. Fig.2 population N (resolve discrepancy) ---------------------------
p("\n[2] Fig.2 population = C1 coded failures (numeric_wrong+defensible+vis_failure")
p("    coded in final_coded) PLUS C1 code_error auto-CD. Format failures excluded.")
c1_coded = fc[fc.condition == "C1"]
c1_code_err = df[(df.condition == "C1") & (df.bucket == "code_error")]
N_fig2 = len(c1_coded) + len(c1_code_err)
p(f"    C1 coded rows in final_coded: {len(c1_coded)}")
p(f"    C1 code_error (auto-CD): {len(c1_code_err)}")
p(f"    ==> Fig.2 N = {N_fig2}")
# class counts
counts = {c: int((c1_coded.final_class == c).sum()) for c in CLASSES}
counts["CD"] += len(c1_code_err)
p(f"    class counts: " + ", ".join(f"{c}={counts[c]} ({100*counts[c]/N_fig2:.1f}%)"
                                    for c in CLASSES))
p(f"    hardcoded_constant within CN: {int(c1_coded.hardcoded.sum())}")

# ---- 3. mechanical lower bound (C1) ---------------------------------------
p("\n[3] Mechanical lower bound (C1, source=='mechanical' only) — kappa-immune")
mech = c1_coded[c1_coded.source == "mechanical"]
p(f"    deterministically settled: {len(mech)}/{len(c1_coded)} coded items")
for c in ("CV", "CN"):
    k = int((mech.final_class == c).sum())
    p(f"    >= {k} C1 failures are {c} confirmed mechanically "
      f"({100*k/N_fig2:.1f}% of Fig.2 N, as a floor)")

# ---- 4. per-coder proportion interval (C1) --------------------------------
p("\n[4] Per-coder proportion interval (C1 coded items with both AI votes)")
both = c1_coded.dropna(subset=["coder_Q", "coder_K"])
p(f"    items with both votes: {len(both)}")
for c in CLASSES:
    q = (both.coder_Q == c).mean() * 100
    l = (both.coder_K == c).mean() * 100
    p(f"    {c}: Q={q:.1f}%  L={l:.1f}%  -> report as {min(q,l):.0f}-{max(q,l):.0f}%")
# kappa
po = (both.coder_Q == both.coder_K).mean()
pe = sum((both.coder_Q == c).mean() * (both.coder_K == c).mean()
         for c in set(both.coder_Q) | set(both.coder_K))
p(f"    Cohen kappa (C1 subset) = {(po-pe)/(1-pe):.3f}; agreement {100*po:.1f}%")
allboth = fc.dropna(subset=["coder_Q", "coder_K"])
po2 = (allboth.coder_Q == allboth.coder_K).mean()
pe2 = sum((allboth.coder_Q == c).mean() * (allboth.coder_K == c).mean()
          for c in set(allboth.coder_Q) | set(allboth.coder_K))
p(f"    Cohen kappa (all 686) = {(po2-pe2)/(1-pe2):.3f}; agreement {100*po2:.1f}%")

# ---- 5. correctness conditional on executable code ------------------------
p("\n[5] Correctness conditional on code that executes (exec_ok==1)")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[(df.condition == cond) & (df.exec_ok == 1)]
    p(f"    {cond}: {s.correct.sum()}/{len(s)} = {100*s.correct.mean():.1f}% "
      f"(unconditional {100*df[df.condition==cond].correct.mean():.1f}%)")

# ---- 6. visible vs silent failures (C1) -----------------------------------
p("\n[6] Visible vs silent failures (C1, n=540)")
c1 = df[df.condition == "C1"]
visible = c1[(c1.bucket == "code_error") |
             ((c1.bucket == "format_failure") & (c1.exec_ok == 0))]
silent = c1[(c1.bucket == "numeric_wrong") & (c1.exec_ok == 1)]
fmt = c1[c1.bucket == "format_failure"]
p(f"    visible (no-code format + code errors): {len(visible)}")
p(f"    silent (executed but numerically wrong): {len(silent)}")
p(f"    format failures total: {len(fmt)} (no-code: {int((fmt.exec_ok==0).sum())})")

# ---- 7. latency truncation cost -------------------------------------------
p("\n[7] Latency truncation cost (fraction of CORRECT generations lost)")
for cut in (45, 60):
    cor = df[df.correct == 1]
    lost = (cor.latency_total_s > cut).mean()
    p(f"    cutoff {cut}s: lose {int((cor.latency_total_s>cut).sum())}/{len(cor)} "
      f"correct = {100*lost:.1f}%")
    for cond in ("C1", "C4"):
        cc = cor[cor.condition == cond]
        p(f"        {cond}: {100*(cc.latency_total_s>cut).mean():.1f}% of its correct lost")
p(f"    overall latency: median {df.latency_total_s.median():.1f}s "
  f"p90 {df.latency_total_s.quantile(.9):.1f}s")

# ---- 8. C3-T3 anomaly CI --------------------------------------------------
p("\n[8] C3-T3 anomaly (19.4% vs C1-T3 25.0%): bootstrap CI on the difference")
t3 = df[df.task_type == "T3"]
c1t3 = t3[t3.condition == "C1"]
c3t3 = t3[t3.condition == "C3"]
m1, lo1, hi1 = cluster_bootstrap_ci(c1t3, "correct", b=10000)
m3, lo3, hi3 = cluster_bootstrap_ci(c3t3, "correct", b=10000)
p(f"    C1-T3 = {100*m1:.1f}% [{100*lo1:.1f},{100*hi1:.1f}]")
p(f"    C3-T3 = {100*m3:.1f}% [{100*lo3:.1f},{100*hi3:.1f}]")
# paired bootstrap on the difference over the 6 T3 tasks
rng = np.random.default_rng(20260610)
tasks = t3.task_id.unique()
gc1 = {t: c1t3[c1t3.task_id == t].correct.values for t in tasks}
gc3 = {t: c3t3[c3t3.task_id == t].correct.values for t in tasks}
diffs = []
for _ in range(10000):
    draw = rng.choice(tasks, len(tasks), replace=True)
    a = np.concatenate([gc3[t] for t in draw]).mean()
    b = np.concatenate([gc1[t] for t in draw]).mean()
    diffs.append(a - b)
dlo, dhi = np.percentile(diffs, [2.5, 97.5])
p(f"    C3-C1 on T3 = {100*(m3-m1):+.1f}pp  CI [{100*dlo:+.1f},{100*dhi:+.1f}]")
p(f"    -> {'within noise (CI spans 0)' if dlo < 0 < dhi else 'NOT within noise'}")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
p(f"\nwrote {OUT}")

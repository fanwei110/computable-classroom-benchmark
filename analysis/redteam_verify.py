"""Verify red-team-flagged checkable facts + run the inference robustness the
reviewers demand (equivalence test for the convention 'null'; leave-one-task-out
for the interaction). Reads runs/results_formal.csv. Writes runs/redteam_stats.txt."""
import io, sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from bootstrap_ci import cluster_bootstrap_ci
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
out = []
def p(s=""): out.append(str(s)); print(s)

df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
fc = pd.read_csv(ROOT / "coding" / "auto" / "final_coded.csv")

p("=== FACT CHECK: Fig.2 denominators 266 / 306 / 686 ===")
c1_coded = (fc.condition == "C1").sum()
c1_codeerr = ((df.condition=="C1") & (df.bucket=="code_error")).sum()
p(f"C1 coded-in-final_coded = {c1_coded}; C1 code_error auto-CD = {c1_codeerr}; "
  f"sum = {c1_coded+c1_codeerr} (should be 306); total coded items all conds = {len(fc)} (686)")

p("\n=== TOST equivalence test: convention main effect (C3 vs C1) ===")
# paired cluster bootstrap of C3-C1 difference over 18 tasks; report 90% CI
# (TOST uses 90% CI for alpha=0.05 two one-sided tests)
rng = np.random.default_rng(20260610)
tasks = sorted(df.task_id.unique())
def cond_task(cond):
    s = df[df.condition==cond]
    return {t: s[s.task_id==t].correct.values for t in tasks}
gc1, gc3, gc2, gc4 = cond_task("C1"), cond_task("C3"), cond_task("C2"), cond_task("C4")
diffs=[]
for _ in range(20000):
    dr = rng.choice(tasks, len(tasks), replace=True)
    diffs.append(np.concatenate([gc3[t] for t in dr]).mean() - np.concatenate([gc1[t] for t in dr]).mean())
lo90, hi90 = np.percentile(diffs, [5, 95])
lo95, hi95 = np.percentile(diffs, [2.5, 97.5])
p(f"C3-C1 diff = {100*np.mean(diffs):+.1f}pp; 90% CI [{100*lo90:+.1f},{100*hi90:+.1f}]; "
  f"95% CI [{100*lo95:+.1f},{100*hi95:+.1f}]")
p(f"  -> equivalence bound: the convention main effect is within "
  f"[{100*lo90:+.1f},{100*hi90:+.1f}] pp at 90% confidence (TOST reading).")

p("\n=== Leave-one-task-out: interaction (C4-C2)-(C3-C1) ===")
def interaction(tasklist):
    a = np.concatenate([gc4[t] for t in tasklist]).mean() - np.concatenate([gc2[t] for t in tasklist]).mean()
    b = np.concatenate([gc3[t] for t in tasklist]).mean() - np.concatenate([gc1[t] for t in tasklist]).mean()
    return a - b
full = interaction(tasks)
p(f"full interaction (pp scale) = {100*full:+.1f}pp")
loo = []
for t in tasks:
    rest = [x for x in tasks if x != t]
    loo.append((t, 100*interaction(rest)))
loo_vals = [v for _, v in loo]
p(f"leave-one-out range: [{min(loo_vals):+.1f}, {max(loo_vals):+.1f}] pp; all same sign: "
  f"{all(v>0 for v in loo_vals)}")
worst = min(loo, key=lambda x: x[1])
p(f"  most influential task (drop -> lowest interaction): {worst[0]} -> {worst[1]:+.1f}pp")

p("\n=== Structure main effect (C2 vs C1) equivalence/size for contrast ===")
d2=[]
for _ in range(20000):
    dr = rng.choice(tasks, len(tasks), replace=True)
    d2.append(np.concatenate([gc2[t] for t in dr]).mean() - np.concatenate([gc1[t] for t in dr]).mean())
p(f"C2-C1 = {100*np.mean(d2):+.1f}pp; 95% CI [{100*np.percentile(d2,2.5):+.1f},{100*np.percentile(d2,97.5):+.1f}]")

(ROOT/"runs"/"redteam_stats.txt").write_text("\n".join(out)+"\n", encoding="utf-8")
p("\nwrote runs/redteam_stats.txt")

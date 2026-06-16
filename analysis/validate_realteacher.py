"""Real-teacher vs persona-simulated validation (paper §IV.C).

Compares, on the SAME 10 tasks and the SAME C1/C3 conditions, the
correctness and chat-mode behavior of generations prompted with real-
instructor phrasings vs the persona-simulated phrasings used in the main
study. A small, non-significant difference validates that the headline
34.3% is not an artifact of AI-simulated phrasing.

Outputs runs/realteacher_validation.txt.
"""

import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from bootstrap_ci import cluster_bootstrap_ci  # noqa: E402

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
TASKS = ["KP1_T1", "KP2_T1", "KP2_T3", "KP3_T1", "KP3_T3",
         "KP4_T1", "KP4_T3", "KP5_T1", "KP5_T3", "KP6_T3"]
out = []


def p(s=""):
    out.append(str(s)); print(s)


# ---- real-teacher rows ----------------------------------------------------
rt = []
for line in (ROOT / "runs" / "raw" / "realteacher" / "realteacher.jsonl").read_text(
        encoding="utf-8").splitlines():
    r = json.loads(line)
    j = r["judge"]
    rt.append({"task_id": r["task_id"], "condition": r["condition"],
               "model": r["model"], "correct": int(j["bucket"] == "correct"),
               "nocode": int(not r["code_extracted"]),
               "clarify": int(j.get("behavior") == "clarify")})
rt = pd.DataFrame(rt)

# ---- persona rows (same tasks, C1/C3) -------------------------------------
res = pd.read_csv(ROOT / "runs" / "results_formal.csv")
pe = res[(res.task_id.isin(TASKS)) & (res.condition.isin(["C1", "C3"]))].copy()

p("=" * 60)
p("REAL-TEACHER vs PERSONA-SIMULATED  (same 10 tasks)")
p("=" * 60)
p(f"real-teacher generations: {len(rt)}  | persona (same tasks): {len(pe)}")

for cond in ("C1", "C3"):
    p(f"\n--- {cond} ---")
    r1 = rt[rt.condition == cond]
    p1 = pe[pe.condition == cond]
    mr, lor, hir = cluster_bootstrap_ci(r1, "correct", b=10000)
    mp, lop, hip = cluster_bootstrap_ci(p1, "correct", b=10000)
    p(f"  real-teacher correct: {r1.correct.sum()}/{len(r1)} = {100*mr:.1f}% "
      f"[{100*lor:.1f},{100*hir:.1f}]")
    p(f"  persona      correct: {p1.correct.sum()}/{len(p1)} = {100*mp:.1f}% "
      f"[{100*lop:.1f},{100*hip:.1f}]")
    p(f"  difference (real-persona): {100*(mr-mp):+.1f} pp")
    # paired bootstrap over the 10 tasks
    rng = np.random.default_rng(20260610)
    gr = {t: r1[r1.task_id == t].correct.values for t in TASKS}
    gp = {t: p1[p1.task_id == t].correct.values for t in TASKS}
    diffs = []
    for _ in range(10000):
        draw = rng.choice(TASKS, len(TASKS), replace=True)
        a = np.concatenate([gr[t] for t in draw]).mean()
        b = np.concatenate([gp[t] for t in draw]).mean()
        diffs.append(a - b)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p(f"  paired-bootstrap CI on difference: [{100*lo:+.1f},{100*hi:+.1f}] pp "
      f"-> {'indistinguishable (spans 0)' if lo < 0 < hi else 'DIFFERENT'}")

# ---- chat-mode behavior ---------------------------------------------------
p("\n--- chat-mode behavior (C1, the diagnostic condition) ---")
r1 = rt[rt.condition == "C1"]
p(f"  real-teacher no-code rate: {100*r1.nocode.mean():.1f}% "
  f"({r1.nocode.sum()}/{len(r1)})")
nc = res[(res.task_id.isin(TASKS)) & (res.condition == "C1")]
nc_rate = ((nc.bucket == "format_failure") & (nc.exec_ok == 0)).mean() if "exec_ok" in nc else np.nan
p(f"  persona no-code (approx, same tasks): "
  f"{100*((nc.bucket=='format_failure')&(nc.exec_ok==0)).mean():.1f}%")
p(f"  clarifying questions (real-teacher, all {len(rt)}): {rt.clarify.sum()}")

# ---- per-task table -------------------------------------------------------
p("\n--- per-task C1 strict correctness (real / persona) ---")
for t in TASKS:
    rr = rt[(rt.task_id == t) & (rt.condition == "C1")].correct.mean()
    pp = pe[(pe.task_id == t) & (pe.condition == "C1")].correct.mean()
    p(f"  {t}: {100*rr:4.0f}% / {100*pp:4.0f}%")

(ROOT / "runs" / "realteacher_validation.txt").write_text("\n".join(out) + "\n",
                                                          encoding="utf-8")
p("\nwrote runs/realteacher_validation.txt")

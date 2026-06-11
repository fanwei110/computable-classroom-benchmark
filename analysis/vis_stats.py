"""Visualization adequacy statistics from the two AI raters.

Rules (disclosed): a figure is adequate iff BOTH raters pass all four
rubric items (conservative consensus; disagreements count as inadequate).
T2 generations that produced no figure file are inadequate by definition.
The 9 interactive HTML figures cannot be rated by the vision models and
are reported separately (not in the adequacy denominator).

Outputs: coding/auto/vis_final.csv + printed stats (incl. kappa on the
binary adequate/inadequate decision over co-rated figures).
"""

import io
import json
import sys
from pathlib import Path

import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
AUTO = ROOT / "coding" / "auto"
FIGS = ROOT / "runs" / "raw" / "formal" / "figures"


def kappa(a, b):
    a, b = pd.Series(a), pd.Series(b)
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in set(a) | set(b))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def load(rater):
    rows = [json.loads(x) for x in
            (AUTO / f"fig_rater_{rater}.jsonl").read_text(encoding="utf-8").splitlines()]
    df = pd.DataFrame(rows).drop_duplicates("run_id", keep="last")
    return df.set_index("run_id")


r1, r2 = load("R1"), load("R2")
res = pd.read_csv(ROOT / "runs" / "results_formal.csv")
t2 = res[res.task_type == "T2"].copy()

html_ids = {p.stem for p in FIGS.glob("*.html")}
rated_ids = set(r1.index) & set(r2.index)

rows = []
for _, r in t2.iterrows():
    rid = r.run_id
    if rid in html_ids:
        status = "html_unrated"
        adequate = None
    elif rid in rated_ids and r1.loc[rid].get("adequate") is not None \
            and r2.loc[rid].get("adequate") is not None:
        a1, a2 = bool(r1.loc[rid]["adequate"]), bool(r2.loc[rid]["adequate"])
        status = "rated"
        adequate = a1 and a2
    else:
        status = "no_figure"
        adequate = False
    rows.append({"run_id": rid, "condition": r.condition, "model": r.model,
                 "status": status, "adequate": adequate,
                 "r1": r1.loc[rid]["adequate"] if rid in r1.index else None,
                 "r2": r2.loc[rid]["adequate"] if rid in r2.index else None})

df = pd.DataFrame(rows)
df.to_csv(AUTO / "vis_final.csv", index=False, encoding="utf-8-sig")

co = df[df.status == "rated"].dropna(subset=["r1", "r2"])
agree = (co.r1.astype(bool) == co.r2.astype(bool)).mean()
print(f"T2 generations: {len(df)}; rated: {(df.status=='rated').sum()}; "
      f"no-figure (inadequate by definition): {(df.status=='no_figure').sum()}; "
      f"interactive HTML (reported separately): {(df.status=='html_unrated').sum()}")
print(f"rater agreement on adequate (binary): {agree*100:.1f}% ; "
      f"kappa = {kappa(co.r1.astype(bool), co.r2.astype(bool)):.3f}")
print(f"R1 adequate rate: {co.r1.astype(bool).mean()*100:.1f}% ; "
      f"R2: {co.r2.astype(bool).mean()*100:.1f}%")

sub = df[df.status != "html_unrated"]
print("\nadequacy (both-rater consensus; no-figure counted inadequate):")
for cond in ("C1", "C2", "C3", "C4"):
    s = sub[sub.condition == cond]
    n_ok = s.adequate.fillna(False).sum()
    print(f"  {cond}: {n_ok}/{len(s)} = {100*n_ok/len(s):.1f}%")
print("\nby model (pooled conditions):")
for m in ("M1", "M2", "M3"):
    s = sub[sub.model == m]
    n_ok = s.adequate.fillna(False).sum()
    print(f"  {m}: {n_ok}/{len(s)} = {100*n_ok/len(s):.1f}%")

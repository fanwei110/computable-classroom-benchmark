"""Aggregate the revision-1 pilot (Creg + C1wS) and assemble the full
wording x scaffold 2x2 (-convention row) against the FORMAL C1/C2 restricted
to the same 6 pilot tasks. Correctness derived exactly as
analysis/aggregate_formal.py: correct = (bucket == 'correct');
exec_ok = has_code and bucket != 'code_error'.
Usage: python rev_pilot_stats.py [--tag rev_pilot]
"""
import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_pilot(tag):
    rows = []
    with open(ROOT / "runs" / "raw" / tag / f"{tag}.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            b = r["judge"]["bucket"]
            rows.append({
                "model": r["model"], "condition": r["condition"],
                "task_id": r["task_id"], "bucket": b,
                "exec_ok": int(r["code_extracted"] and b != "code_error"),
                "correct": int(b == "correct"),
            })
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="rev_pilot")
    args = ap.parse_args()

    pilot = load_pilot(args.tag)
    tasks = sorted(pilot.task_id.unique())
    formal = pd.read_csv(ROOT / "runs" / "results_formal.csv")
    fsub = formal[formal.task_id.isin(tasks)]

    print(f"pilot tasks: {tasks}")
    print(f"pilot N={len(pilot)}  (per condition: "
          f"{pilot.groupby('condition').size().to_dict()})\n")

    def pct(df):
        return df.correct.mean() * 100

    # ---- pooled 2x2 (wording x scaffold), -convention row -------------------
    c1 = pct(fsub[fsub.condition == "C1"])
    c2 = pct(fsub[fsub.condition == "C2"])
    creg = pct(pilot[pilot.condition == "Creg"])
    c1ws = pct(pilot[pilot.condition == "C1wS"])
    print("=== pooled strict correctness (%, same 6 tasks) ===")
    print(f"                     no scaffold   + scaffold")
    print(f"improvised wording   C1  = {c1:5.1f}   C1wS = {c1ws:5.1f}   (formal | NEW)")
    print(f"regularized wording  Creg= {creg:5.1f}   C2   = {c2:5.1f}   (NEW | formal)")
    print(f"\nwording effect  (no scaffold): Creg-C1  = {creg-c1:+5.1f} pp")
    print(f"wording effect  (+ scaffold):  C2-C1wS  = {c2-c1ws:+5.1f} pp")
    print(f"scaffold effect (improvised):  C1wS-C1  = {c1ws-c1:+5.1f} pp")
    print(f"scaffold effect (regularized): C2-Creg  = {c2-creg:+5.1f} pp")
    print(f"bundle total (C2-C1)         = {c2-c1:+5.1f} pp")

    # ---- per model ----------------------------------------------------------
    print("\n=== per model (%, same 6 tasks) ===")
    print(f"{'model':6} {'C1':>6} {'C1wS':>6} {'Creg':>6} {'C2':>6}")
    for m in ("M1", "M2", "M3"):
        row = [pct(fsub[(fsub.condition == c) & (fsub.model == m)]) for c in ("C1", "C2")]
        prow = [pct(pilot[(pilot.condition == c) & (pilot.model == m)])
                for c in ("C1wS", "Creg")]
        print(f"{m:6} {row[0]:6.1f} {prow[0]:6.1f} {prow[1]:6.1f} {row[1]:6.1f}")

    # ---- executability + bucket mix for the new cells -----------------------
    print("\n=== new cells: executability and bucket mix ===")
    for c in ("Creg", "C1wS"):
        sub = pilot[pilot.condition == c]
        print(f"{c}: exec_ok={sub.exec_ok.mean()*100:.1f}%  "
              f"buckets={sub.bucket.value_counts().to_dict()}")

    # persist tidy csv for later folding into stats
    out = ROOT / "runs" / f"{args.tag}_tidy.csv"
    pilot.to_csv(out, index=False, encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()

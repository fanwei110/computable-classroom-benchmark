"""R1.4: full reconciliation ("accounting") of the 2,160 formal generations
across mutually exclusive outcome buckets, per condition -- so every
percentage in the paper has an auditable numerator/denominator.

Bucket definitions (frozen judge, aggregate_formal.py conventions):
  format_failure : no code extracted, or executed without populating `result`
                   (output-contract violation); never counted as numeric_wrong
  code_error     : extracted code crashed
  numeric_wrong  : executed, populated result, failed the tolerance test
  vis_failure    : T2 numeric pass but figure inadequate / missing
  defensible     : T3 alternative-declared-convention tier (not strict-correct)
  correct        : strict numerical correctness (the paper's headline metric)
Derived: exec_ok = code extracted and bucket != code_error.
Output -> runs/accounting_table.txt
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "accounting_table.txt"

df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
lines = []


def say(s=""):
    print(s)
    lines.append(s)


say("=== Reconciliation of the 2,160 formal generations (auditable) ===")
say(f"total rows: {len(df)}  (18 tasks x 4 conditions x 3 models x 10 reps)")
say()

buckets = ["format_failure", "code_error", "numeric_wrong", "vis_failure",
           "defensible", "correct"]
say(f"{'condition':10} " + " ".join(f"{b[:12]:>13}" for b in buckets)
    + f" {'total':>6} {'exec_ok':>8} {'correct%':>9}")
for c in ("C1", "C2", "C3", "C4"):
    sub = df[df.condition == c]
    cnt = sub.bucket.value_counts()
    row = " ".join(f"{cnt.get(b, 0):>13}" for b in buckets)
    say(f"{c:10} {row} {len(sub):>6} {sub.exec_ok.sum():>8} "
        f"{sub.correct.mean()*100:>8.1f}")
say()
say("column definitions: mutually exclusive primary buckets; correct% = "
    "correct/total (strict tier). exec_ok = code extracted & no crash.")
say()

say("--- format_failure split (mechanical): no runnable code vs "
    "executed-but-no-`result` ---")
for c in ("C1", "C2", "C3", "C4"):
    sub = df[(df.condition == c) & (df.bucket == "format_failure")]
    say(f"{c}: format_failure={len(sub)}  no-code={int((sub.exec_ok == 0).sum())}"
        f"  executed-but-no-result={int((sub.exec_ok == 1).sum())}")
say()

say("--- T3 tiers (strict vs defensible), per condition ---")
t3 = df[df.task_id.str.endswith("_T3")]
for c in ("C1", "C2", "C3", "C4"):
    sub = t3[t3.condition == c]
    say(f"{c}: n={len(sub)}  strict={(sub.bucket=='correct').mean()*100:.1f}%  "
        f"defensible-tier-only={(sub.bucket=='defensible').sum()}  "
        f"strict+defensible={(sub.bucket.isin(['correct','defensible'])).mean()*100:.1f}%")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"\nwrote {OUT}")

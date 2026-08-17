"""Phase-D human validation of the error coding.

Reads the two completed blind human-coder sheets (coding/coder_C.xlsx and
coder_D.xlsx) and compares them to each other and to the automated protocol
(coding/auto/final_coded.csv). The sheets contain the 286 batch-1 items:
266 C1 items and 20 C4 items. The manuscript's validation estimand is the C1
subset, selected by joining the public blind_id metadata in final_coded.csv.
Reports, over that analysis subset:
  - inter-coder agreement (percent, Cohen's kappa, Gwet's AC1);
  - human-consensus vs automated-final agreement (percent, kappa) — the number
    that converts "AI-coded-by-AI" into "human-validated".
Writes runs/human_coding_stats.txt and coding/human_disagreements.csv (for the
two coders to resolve). Degrades gracefully until the sheets are filled.

Usage:  python analysis/human_coding_stats.py --condition C1
"""
import io, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
out = []
def p(s=""): out.append(str(s)); print(s)

CLASSES = ["CD", "CV", "CN", "VZ"]


def load_coder(path):
    df = pd.read_excel(path)
    pc = [c for c in df.columns if "primary_class" in str(c)][0]
    df = df.rename(columns={pc: "cls"})
    df["cls"] = df["cls"].astype(str).str.strip().str.upper()
    df.loc[~df["cls"].isin(CLASSES), "cls"] = np.nan
    return df[["blind_id", "cls"]]


def cohen_kappa(a, b):
    labs = sorted(set(a) | set(b))
    idx = {l: i for i, l in enumerate(labs)}
    n = len(a)
    po = np.mean([x == y for x, y in zip(a, b)])
    pa = np.array([sum(x == l for x in a) / n for l in labs])
    pb = np.array([sum(x == l for x in b) / n for l in labs])
    pe = float(np.dot(pa, pb))
    return (po - pe) / (1 - pe) if pe < 1 else 1.0, po


def gwet_ac1(a, b):
    labs = sorted(set(a) | set(b))
    n = len(a)
    po = np.mean([x == y for x, y in zip(a, b)])
    pi = np.array([(sum(x == l for x in a) + sum(x == l for x in b)) / (2 * n) for l in labs])
    K = len(labs)
    pe = float(np.sum(pi * (1 - pi)) / (K - 1)) if K > 1 else 0.0
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


p("================================================================")
p("PHASE-D HUMAN VALIDATION OF ERROR CODING")
p("================================================================")

import argparse
_ap = argparse.ArgumentParser()
_ap.add_argument("--a", default="coder_C.xlsx", help="first completed coder sheet")
_ap.add_argument("--b", default="coder_D.xlsx", help="second completed coder sheet")
_ap.add_argument("--condition", default="C1",
                 help="condition subset in coding/auto/final_coded.csv; use 'all' for all 286 rows")
_args = _ap.parse_args()
try:
    A = load_coder(ROOT / "coding" / _args.a)
    B = load_coder(ROOT / "coding" / _args.b)
    p(f"coders: A={_args.a}  B={_args.b}")
except FileNotFoundError as e:
    p(f"coder sheet not found: {e}"); sys.exit(0)

m = A.merge(B, on="blind_id", suffixes=("_A", "_B"))
both_all = m.dropna(subset=["cls_A", "cls_B"]).reset_index(drop=True)

# 不能按“前20行”删除：20条校准练习另存于 coding/calibration/，并不在
# coder_C/D 中。两张正式表的 286 行由 C1=266 与 C4=20 构成，必须借助
# 已公开的 final_coded.csv 按 condition 筛选，才能复现论文的 C1 估计量。
meta = pd.read_csv(ROOT / "coding" / "auto" / "final_coded.csv")[["blind_id", "condition"]]
both = both_all.merge(meta, on="blind_id", how="left", validate="one_to_one")
if _args.condition.lower() != "all":
    both = both[both["condition"] == _args.condition].reset_index(drop=True)

p(f"\nsheet rows: {len(m)} ; coded by BOTH humans: {len(both_all)}")
p(f"analysis subset: condition={_args.condition} ; n={len(both)}")
if len(both) == 0:
    p(f"\n>>> Human coding not done yet. Fill {_args.a} / {_args.b} "
      "(column primary_class), then re-run.")
    (ROOT / "runs" / "human_coding_stats.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    sys.exit(0)

a, b = list(both["cls_A"]), list(both["cls_B"])

# inter-coder agreement
k, po = cohen_kappa(a, b)
ac1 = gwet_ac1(a, b)
p(f"\n[A vs B, n={len(both)}] percent agreement={100*po:.1f}%  "
  f"Cohen kappa={k:.3f}  Gwet AC1={ac1:.3f}")
p("  class distribution (A / B):")
for c in CLASSES:
    p(f"    {c}: {sum(x==c for x in a)} / {sum(x==c for x in b)}")

# disagreements -> csv for resolution
dis = both[both["cls_A"] != both["cls_B"]][["blind_id", "cls_A", "cls_B"]]
dis.to_csv(ROOT / "coding" / "human_disagreements.csv", index=False)
p(f"\n{len(dis)} disagreements written to coding/human_disagreements.csv")

# human consensus (agreed rows) vs automated final_class
agreed = both[both["cls_A"] == both["cls_B"]][["blind_id", "cls_A"]].rename(columns={"cls_A": "human"})
auto = pd.read_csv(ROOT / "coding" / "auto" / "final_coded.csv")[["blind_id", "final_class"]]
hv = agreed.merge(auto, on="blind_id").dropna()
if len(hv):
    hk, hpo = cohen_kappa(list(hv["human"]), list(hv["final_class"].str.upper()))
    p(f"\n[human-consensus vs automated-final, n={len(hv)}] "
      f"percent={100*hpo:.1f}%  kappa={hk:.3f}")
    p("  -> this is the human-validation number for the manuscript (SS IV.D / V.B).")

(ROOT / "runs" / "human_coding_stats.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
p("\nwrote runs/human_coding_stats.txt")

"""核验可审计分母，并重算已注册对比、区间与任务留一法。

读取 runs/results_formal.csv，写入 runs/redteam_stats.txt。约定效应没有预设
等效界值，因此这里只报告效应区间，不把区间误称为 TOST 或等效性检验。
"""

import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
out = []


def p(s=""):
    """同步打印并保存一行审计结果。"""
    out.append(str(s))
    print(s)


df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
fc = pd.read_csv(ROOT / "coding" / "auto" / "final_coded.csv")

p("=== FACT CHECK: Fig.2 denominators 266 / 306 / 686 ===")
c1_coded = int((fc.condition == "C1").sum())
c1_codeerr = int(((df.condition == "C1") & (df.bucket == "code_error")).sum())
p(f"C1 coded-in-final_coded = {c1_coded}; C1 code_error auto-CD = {c1_codeerr}; "
  f"sum = {c1_coded+c1_codeerr} (should be 306); total coded items all conds = {len(fc)} (686)")

# 每个任务在各单元的重复数相同；联合重抽18个任务即可保持四单元配对结构。
rng = np.random.default_rng(20260610)
rates = (
    df.groupby(["task_id", "condition"]).correct.mean().unstack("condition")
    [["C1", "C2", "C3", "C4"]]
)
tasks = list(rates.index)
idx = rng.integers(0, len(tasks), size=(20_000, len(tasks)))
vectors = {
    "H1 bundle C4-C1": (rates["C4"] - rates["C1"]).to_numpy(),
    "H2a convention-only C3-C1": (rates["C3"] - rates["C1"]).to_numpy(),
    "H2b convention-with-structure C4-C2": (rates["C4"] - rates["C2"]).to_numpy(),
    "structural contrast C2-C1": (rates["C2"] - rates["C1"]).to_numpy(),
}
vectors["factorial interaction (C4-C2)-(C3-C1)"] = (
    vectors["H2b convention-with-structure C4-C2"]
    - vectors["H2a convention-only C3-C1"]
)

p("\n=== REGISTERED AND FACTORIAL CONTRASTS: paired task-cluster bootstrap ===")
draws = {}
for label, vector in vectors.items():
    boot = vector[idx].mean(axis=1) * 100
    draws[label] = boot
    lo95, hi95 = np.percentile(boot, [2.5, 97.5])
    p(f"{label}: {100 * vector.mean():+.1f} pp; 95% CI [{lo95:+.1f}, {hi95:+.1f}]")

conv_label = "H2a convention-only C3-C1"
lo90, hi90 = np.percentile(draws[conv_label], [5, 95])
p(f"C3-C1 additional 90% interval: [{lo90:+.1f}, {hi90:+.1f}] pp.")
p("No equivalence margin was prespecified; this is an uncertainty bound, not a "
  "TOST or an equivalence result.")

p("\n=== Leave-one-task-out: interaction (C4-C2)-(C3-C1) ===")
interaction_vector = vectors["factorial interaction (C4-C2)-(C3-C1)"]
p(f"full interaction (pp scale) = {100 * interaction_vector.mean():+.1f}pp")
loo = []
for i, task_id in enumerate(tasks):
    loo.append((task_id, 100 * np.delete(interaction_vector, i).mean()))
loo_vals = [v for _, v in loo]
p(f"leave-one-out range: [{min(loo_vals):+.1f}, {max(loo_vals):+.1f}] pp; all same sign: "
  f"{all(v > 0 for v in loo_vals)}")
worst = min(loo, key=lambda x: x[1])
p(f"  most influential task (drop -> lowest interaction): {worst[0]} -> {worst[1]:+.1f}pp")

(ROOT / "runs" / "redteam_stats.txt").write_text(
    "\n".join(out) + "\n", encoding="utf-8"
)
p("\nwrote runs/redteam_stats.txt")

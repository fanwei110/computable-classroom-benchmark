"""L2 精修补算：
[A] 任务级可靠性（meso 第4条）——C4/C1 下 完美单元(task×model,10/10) 计数、
    任务级(30 reps) 完美计数、按 C4 正确率排名的最可靠/最脆弱任务。
[B] 交互项稳健性——任务级交互差值的 Rademacher 符号翻转检验。
[C] Firth 惩罚 logistic 复算交互 OR（缺包则降级为普通 logistic，标注）。
读取 runs/results_formal.csv，写 runs/l2_stats.txt。所有数字仅供回填，不改既有真值。
"""
import io, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
out = []
def p(s=""): out.append(str(s)); print(s)

df = pd.read_csv(ROOT / "runs" / "results_formal.csv")

KP = {"KP1": "均值-方差有效前沿", "KP2": "CAPM/SML", "KP3": "债券久期凸性",
      "KP4": "Black-Scholes/希腊字母", "KP5": "VaR", "KP6": "夏普/归因"}
def label(tid):
    kp, tt = tid.split("_")
    return f"{tid}({KP.get(kp, kp)}·{tt})"

p("================================================================")
p("L2 STATS  (task-level reliability + interaction robustness)")
p("================================================================")

# ---------- [A] 任务级可靠性 ----------
p("\n[A] Task-level reliability (cells = task x model, 10 reps each)")
for cond in ["C1", "C4"]:
    s = df[df.condition == cond]
    cell = s.groupby(["task_id", "model"]).correct.mean()
    perfect_cells = int((cell == 1.0).sum())
    n_cells = cell.shape[0]
    task_pool = s.groupby("task_id").correct.mean()
    perfect_tasks = int((task_pool == 1.0).sum())
    p(f"  {cond}: perfect cells (10/10) = {perfect_cells}/{n_cells} ; "
      f"tasks perfect across all {s.groupby('task_id').size().iloc[0]} reps = "
      f"{perfect_tasks}/{task_pool.shape[0]}")

# C4 ranking
c4 = df[df.condition == "C4"].groupby("task_id").correct.mean().sort_values(ascending=False)
c4_cellperfect = (df[df.condition == "C4"].groupby(["task_id", "model"]).correct.mean() == 1.0) \
    .groupby("task_id").sum().astype(int)
p("\n  C4 per-task pooled correctness (30 reps), most reliable -> most brittle:")
for tid, v in c4.items():
    p(f"    {label(tid):32s} {100*v:5.1f}%   perfect models: {c4_cellperfect[tid]}/3")
p(f"\n  Most reliable under C4 (>=90% AND >=2/3 models perfect): "
  + ", ".join(label(t) for t in c4.index if c4[t] >= 0.90 and c4_cellperfect[t] >= 2))
p(f"  Most brittle under C4 (<80%): "
  + ", ".join(label(t) for t in c4.index if c4[t] < 0.80))

# ---------- [B] 任务级交互差值的符号翻转检验 ----------
p("\n[B] Interaction (C4-C2)-(C3-C1): Rademacher sign-flip test over tasks")
tasks = sorted(df.task_id.unique())
def cmean(cond, t):
    s = df[(df.condition == cond) & (df.task_id == t)]
    return s.correct.mean()
d = np.array([(cmean("C4", t) - cmean("C2", t)) - (cmean("C3", t) - cmean("C1", t)) for t in tasks])
n = len(d)
obs = d.mean()
se = d.std(ddof=1) / np.sqrt(n)
t_obs = obs / se
rng = np.random.default_rng(20260617)
B = 10000
# 在零均值假设下，对18个任务级交互差值随机翻转符号。
tstar = np.empty(B)
for b in range(B):
    w = rng.choice([-1.0, 1.0], size=n)
    ds = w * d                      # impose null (no recentering by mean)
    tstar[b] = ds.mean() / (ds.std(ddof=1) / np.sqrt(n))
pval = float(np.mean(np.abs(tstar) >= abs(t_obs)))
p(f"  interaction point = {100*obs:+.1f}pp ; cluster SE = {100*se:.1f}pp ; t = {t_obs:.2f}")
p(f"  Rademacher sign-flip (B={B}) two-sided p = {pval:.4f}  (n_tasks={n})")

# ---------- [C] Firth (or fallback) interaction OR ----------
p("\n[C] Interaction odds ratio: Firth-penalized logistic (fallback: plain logistic)")
d2 = df.copy()
d2["conv"] = d2.condition.isin(["C3", "C4"]).astype(int)
d2["struct"] = d2.condition.isin(["C2", "C4"]).astype(int)
d2["inter"] = d2.conv * d2.struct
X = d2[["conv", "struct", "inter"]].values
y = d2["correct"].values
method = None
try:
    from firthlogist import FirthLogisticRegression
    m = FirthLogisticRegression()
    m.fit(X, y)
    coef = dict(zip(["conv", "struct", "inter"], m.coef_))
    ci = m.ci_  # 95% CI per coef
    inter_idx = 2
    p(f"  [Firth] interaction log-OR = {coef['inter']:+.3f}  OR = {np.exp(coef['inter']):.2f}  "
      f"95% CI OR [{np.exp(ci[inter_idx][0]):.2f},{np.exp(ci[inter_idx][1]):.2f}]")
    method = "firth"
except Exception as e:
    p(f"  [Firth unavailable: {type(e).__name__}] -> fallback to plain logistic (statsmodels)")
    import statsmodels.api as sm
    Xc = sm.add_constant(d2[["conv", "struct", "inter"]])
    res = sm.Logit(y, Xc).fit(disp=0)
    b = res.params["inter"]; lo, hi = res.conf_int().loc["inter"]
    p(f"  [plain logit] interaction log-OR = {b:+.3f}  OR = {np.exp(b):.2f}  "
      f"95% CI OR [{np.exp(lo):.2f},{np.exp(hi):.2f}]  (model-clustering ignored)")
    method = "plain"

(ROOT / "runs" / "l2_stats.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
p(f"\nwrote runs/l2_stats.txt  (interaction method: {method})")

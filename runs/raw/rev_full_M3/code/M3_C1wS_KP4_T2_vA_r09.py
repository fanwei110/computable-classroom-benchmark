"""
Black-Scholes 欧式期权 Delta 随标的价格变化
课堂演示用：自包含、可复现
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# -------------------- 参数（可调） --------------------
K = 97.5          # 行权价
r = 0.043         # 无风险利率（年化）
T = 0.58          # 剩余期限（年）
S_grid = np.linspace(70, 140, 7 * 70 + 1)   # 70 -> 140，步长 0.1
SIGMAS = [0.15, 0.276, 0.40]                # 波动率参数可调

# -------------------- Black-Scholes 闭式解 --------------------
def bs_d1(S, K, r, T, sigma):
    S = np.asarray(S, dtype=float)
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def bs_call_delta(S, K, r, T, sigma):
    """欧式看涨期权 delta = N(d1)"""
    return norm.cdf(bs_d1(S, K, r, T, sigma))

def bs_put_delta(S, K, r, T, sigma):
    """欧式看跌期权 delta = N(d1) - 1（如需可启用）"""
    return bs_call_delta(S, K, r, T, sigma) - 1.0

# -------------------- 步骤1：在每个波动率上计算 delta --------------------
delta_table = pd.DataFrame({"S": S_grid})
for sigma in SIGMAS:
    delta_table[f"delta_sigma_{sigma:.3f}"] = bs_call_delta(S_grid, K, r, T, sigma)

# -------------------- 步骤2：画三条曲线 --------------------
plt.rcParams.update({"font.size": 11})
fig, ax = plt.subplots(figsize=(9, 5.5))

colors = ["#1f77b4", "#d62728", "#2ca02c"]
for sigma, c in zip(SIGMAS, colors):
    col = f"delta_sigma_{sigma:.3f}"
    ax.plot(delta_table["S"], delta_table[col],
            color=c, lw=2.0,
            label=rf"$\sigma$ = {sigma*100:.1f}%")

# 关键参考线
ax.axvline(K, color="gray", ls="--", lw=1.0, alpha=0.7,
           label=rf"行权价 $K$ = {K}")
ax.axhline(0.5, color="gray", ls=":", lw=1.0, alpha=0.5)

ax.set_xlabel("标的价格 S")
ax.set_ylabel(r"Call Delta  $N(d_1)$")
ax.set_title(rf"欧式看涨期权 Delta 随标的价格变化"
             rf"\n($K$={K}, $r$={r*100:.1f}%, $T$={T} 年)")
ax.set_xlim(70, 140)
ax.set_ylim(-0.02, 1.02)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left", framealpha=0.9)

# 在 S=110, sigma=27.6% 处标注（步骤3的值）
delta_s110 = float(bs_call_delta(110.0, K, r, T, 0.276))
ax.scatter([110.0], [delta_s110], color="black", zorder=5)
ax.annotate(rf"S=110, $\sigma$=27.6%: $\Delta$={delta_s110:.4f}",
            xy=(110.0, delta_s110),
            xytext=(78, delta_s110 + 0.18),
            arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

fig.tight_layout()

# -------------------- 步骤3：报告 S=110, sigma=27.6% 的 delta --------------------
print(f"Delta(S=110, sigma=27.6%) = {delta_s110:.6f}")

# -------------------- 步骤4：保存图形并填充 result --------------------
figure_path = "bs_delta_vs_S.png"
fig.savefig(figure_path, dpi=150, bbox_inches="tight")
plt.close(fig)

result = {
    "delta_at_s110": delta_s110,
    "figure_path": figure_path,
}

# 控制台复核
print("\nresult =")
for k, v in result.items():
    print(f"  {k!r}: {v}")

# 同时展示一小段 delta 表，便于课堂核对
print("\nDelta 表（节选）:")
print(delta_table.iloc[::len(delta_table)//7].to_string(index=False,
        float_format=lambda x: f"{x:.4f}"))

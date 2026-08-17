import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 可调参数 ============
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
S_min, S_max = 70, 140  # 标的价格范围
vol_list = [0.15, 0.276, 0.40]  # 波动率参数（可调）
# ================================

def bs_call_delta(S, K, r, T, sigma):
    """Black-Scholes 欧式看涨期权 Delta"""
    S = np.asarray(S, dtype=float)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

S_range = np.linspace(S_min, S_max, 500)

# ---------- 绘图 ----------
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for sigma, c in zip(vol_list, colors):
    delta_vals = bs_call_delta(S_range, K, r, T, sigma)
    ax.plot(S_range, delta_vals, color=c, linewidth=2,
            label=f'σ = {sigma*100:.1f}%')

ax.axvline(x=K, color='grey', linestyle='--', linewidth=0.8, label=f'行权价 K = {K}')
ax.set_xlabel('标的价格 S', fontsize=13)
ax.set_ylabel('Delta', fontsize=13)
ax.set_title(f'看涨期权 Delta 随标的价格变化\n(K={K}, r={r*100}%, T={T}年)', fontsize=14)
ax.legend(fontsize=11, loc='upper left')
ax.set_ylim(-0.05, 1.05)
ax.grid(True, alpha=0.3)

figure_path = 'delta_vs_spot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- 计算指定点 Delta ----------
delta_at_s110 = float(bs_call_delta(110, K, r, T, 0.276))
print(f"S=110, σ=27.6% 时的 Delta = {delta_at_s110:.6f}")

# ---------- 输出契约 ----------
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

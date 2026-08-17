import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ============ 可调参数 ============
K = 97.5            # 行权价
r = 0.043           # 无风险利率
T = 0.58            # 剩余期限（年）
sigma_list = [0.15, 0.276, 0.40]  # 波动率列表，可自由调整

# 标的价格范围
S_range = np.linspace(70, 140, 500)

# ============ Black-Scholes Call Delta ============
def bs_call_delta(S, K, T, r, sigma):
    """计算欧式看涨期权的Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ============ 计算 S=110, sigma=27.6% 时的 Delta ============
target_S = 110
target_sigma = 0.276
delta_at_s110 = bs_call_delta(target_S, K, T, r, target_sigma)
print(f"标的价={target_S}, 波动率={target_sigma*100}% 时, Call Delta = {delta_at_s110:.6f}")

# ============ 绘图 ============
fig, ax = plt.subplots(figsize=(10, 6))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
for i, sigma in enumerate(sigma_list):
    deltas = bs_call_delta(S_range, K, T, r, sigma)
    ax.plot(S_range, deltas, color=colors[i], linewidth=2,
            label=f'σ = {sigma*100:.1f}%')

# 标记行权价位置
ax.axvline(x=K, color='gray', linestyle='--', linewidth=1, alpha=0.7, label=f'行权价 K = {K}')

# 标记目标点 (S=110, sigma=27.6%)
ax.plot(target_S, delta_at_s110, 'ro', markersize=8, zorder=5)
ax.annotate(f'S=110, σ=27.6%\nΔ={delta_at_s110:.4f}',
            xy=(target_S, delta_at_s110),
            xytext=(target_S + 5, delta_at_s110 - 0.12),
            fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

ax.set_xlabel('标的价格 (S)', fontsize=13)
ax.set_ylabel('Call Delta', fontsize=13)
ax.set_title(f'Delta 随标的价变化  (K={K}, r={r*100}%, T={T}年)', fontsize=14)
ax.legend(fontsize=11, loc='upper left')
ax.set_xlim(70, 140)
ax.set_ylim(-0.05, 1.05)
ax.grid(True, alpha=0.3)
ax.tick_params(labelsize=11)

# 保存图片
fig_path = os.path.join(os.getcwd(), 'delta_vs_price.png')
fig.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ============ 输出契约 ============
result = {
    'delta_at_s110': round(delta_at_s110, 6),
    'figure_path': fig_path
}

print(f"\n结果字典: {result}")

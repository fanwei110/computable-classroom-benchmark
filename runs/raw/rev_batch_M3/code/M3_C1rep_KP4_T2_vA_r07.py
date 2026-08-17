import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==================== 可调参数 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限(年)
S_min, S_max = 70, 140   # 标的价格范围

# 波动率参数(可调)
volatilities = [0.15, 0.276, 0.40]
# =================================================

S_range = np.linspace(S_min, S_max, 1000)

def bs_call_delta(S, K, r, T, sigma):
    """Black-Scholes 看涨期权 Delta"""
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 计算标的=110、波动率=27.6%时的delta
delta_at_s110 = bs_call_delta(110, K, r, T, 0.276)

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
for sigma, color in zip(volatilities, colors):
    deltas = bs_call_delta(S_range, K, r, T, sigma)
    ax.plot(S_range, deltas, color=color, linewidth=2, label=f'σ = {sigma*100:.1f}%')

ax.axvline(x=K, color='gray', linestyle='--', alpha=0.5, label=f'行权价 K = {K}')
ax.set_xlabel('标的价格 (S)', fontsize=13)
ax.set_ylabel('Delta', fontsize=13)
ax.set_title(f'看涨期权 Delta 随标的价格变化\n(K={K}, r={r*100}%, T={T}yr)', fontsize=14)
ax.legend(fontsize=11, loc='upper left')
ax.set_ylim(-0.05, 1.05)
ax.grid(True, alpha=0.3)

plt.tight_layout()
figure_path = 'delta_vs_price.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.show()

# 存入结果字典
result = {
    'delta_at_s110': round(delta_at_s110, 6),
    'figure_path': figure_path
}

print(f"标的=110, 波动率=27.6% 时的 Delta = {delta_at_s110:.6f}")
print(f"图片已保存至: {figure_path}")
print(f"result = {result}")

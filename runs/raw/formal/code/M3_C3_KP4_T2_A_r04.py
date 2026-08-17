import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==================== 可调参数 ====================
K = 97.5            # 行权价
r = 0.043           # 无风险利率（连续复利，小数表示）
T = 0.58            # 剩余期限（年）
volatilities = [0.15, 0.276, 0.40]  # 可调波动率参数（小数表示）
# =================================================

# 标的价格范围
S_range = np.linspace(70, 140, 1000)

# Black-Scholes 欧式看涨期权 Delta
def bs_call_delta(S, K, r, sigma, T):
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 绘图
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#1f77b4', '#2ca02c', '#d62728']
labels = [f'σ = {sigma*100:.1f}%' for sigma in volatilities]

for sigma, color, label in zip(volatilities, colors, labels):
    deltas = bs_call_delta(S_range, K, r, sigma, T)
    ax.plot(S_range, deltas, color=color, linewidth=2, label=label)

ax.axvline(x=K, color='gray', linestyle='--', alpha=0.5, linewidth=1, label=f'K = {K}')
ax.set_xlabel('Underlying Price', fontsize=13)
ax.set_ylabel('Delta', fontsize=13)
ax.set_title('Call Option Delta vs Underlying Price\n'
             f'K={K}, r={r*100}%, T={T}yr', fontsize=14)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_xlim(70, 140)
ax.set_ylim(-0.05, 1.05)

figure_path = 'delta_vs_price.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 计算 S=110, sigma=27.6% 时的 delta
delta_at_s110 = bs_call_delta(110, K, r, 0.276, T)

# 存入结果字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(f"Delta at S=110, σ=27.6%: {delta_at_s110:.6f}")
print(f"Figure saved to: {figure_path}")

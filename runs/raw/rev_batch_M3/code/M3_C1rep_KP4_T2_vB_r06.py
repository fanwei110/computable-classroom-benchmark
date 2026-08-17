import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# ============ 参数设定 ============
K = 97.5          # 行权价
r = 0.043          # 无风险利率
T = 0.58           # 到期时间（年）
S_range = np.linspace(70, 140, 700)  # 标的价格范围
vol_list = [0.15, 0.276, 0.40]        # 三条波动率曲线

# ============ Black-Scholes Call Delta ============
def bs_call_delta(S, K, r, T, sigma):
    """计算欧式看涨期权的Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ============ 绘制Delta曲线 ============
fig, ax = plt.subplots(figsize=(10, 6))

for sigma in vol_list:
    deltas = bs_call_delta(S_range, K, r, T, sigma)
    ax.plot(S_range, deltas, linewidth=2, label=f'σ = {sigma*100:.1f}%')

# 标记S=110的位置
ax.axvline(x=110, color='gray', linestyle='--', alpha=0.5, linewidth=1)
ax.annotate('S=110', xy=(110, 0.02), fontsize=10, color='gray')

ax.set_xlabel('Underlying Price (S)', fontsize=12)
ax.set_ylabel('Delta', fontsize=12)
ax.set_title('Call Option Delta Curves\n(K=97.5, r=4.3%, T=0.58)', fontsize=14)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3)
ax.set_ylim(-0.02, 1.02)

plt.tight_layout()
fig_path = os.path.abspath('delta_curves.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ============ 计算S=110, vol=27.6%的Delta ============
delta_at_s110 = bs_call_delta(110, K, r, T, 0.276)

print(f"Delta at S=110, σ=27.6%: {delta_at_s110:.6f}")
print(f"d1 = {((np.log(110/97.5) + (r + 0.5*0.276**2)*T) / (0.276*np.sqrt(T))):.6f}")
print(f"Figure saved at: {fig_path}")

# ============ 输出契约 ============
result = {
    'delta_at_s110': round(float(delta_at_s110), 6),
    'figure_path': fig_path
}

print(f"\nresult = {result}")

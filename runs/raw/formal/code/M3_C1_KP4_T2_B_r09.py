import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 参数设置（vol可在此调整）====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 到期时间（年）
S_range = np.linspace(70, 140, 1000)  # 标的价格范围
vols = [0.15, 0.276, 0.40]            # 三条波动率曲线（可调）
# =================================================================

def bs_call_delta(S, K, r, T, sigma):
    """Black-Scholes 欧式看涨期权 Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ---------- 计算指定点位 Delta ----------
S_target = 110
vol_target = 0.276
delta_at_s110 = bs_call_delta(S_target, K, r, T, vol_target)

# ---------- 绘图 ----------
plt.figure(figsize=(10, 6))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for vol, color in zip(vols, colors):
    deltas = bs_call_delta(S_range, K, r, T, vol)
    plt.plot(S_range, deltas, color=color, linewidth=2, label=f'σ = {vol*100:.1f}%')

# 标注 S=110 的参考线
plt.axvline(x=110, color='gray', linestyle='--', alpha=0.5, linewidth=1)
plt.scatter([110], [delta_at_s110], color='red', zorder=5, s=60)
plt.annotate(f'S=110, Δ={delta_at_s110:.4f}',
             xy=(110, delta_at_s110),
             xytext=(115, delta_at_s110 - 0.08),
             fontsize=10, color='red',
             arrowprops=dict(arrowstyle='->', color='red'))

plt.axhline(y=0.5, color='gray', linestyle=':', alpha=0.3)
plt.xlabel('标的资产价格 S', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title(f'看涨期权 Delta 曲线  (K={K}, r={r*100}%, T={T}年)', fontsize=14)
plt.legend(fontsize=11, loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()

figure_path = 'delta_curves.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ---------- 输出结果 ----------
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(result)

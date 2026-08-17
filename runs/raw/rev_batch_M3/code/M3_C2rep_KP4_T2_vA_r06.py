import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def bs_call_delta(S, K, T, r, sigma):
    """
    计算不分红欧式看涨期权的 Delta (Black-Scholes 闭式解)
    S: 标的价格 (可以是数组)
    K: 行权价
    T: 剩余期限 (年)
    r: 无风险利率 (连续复利)
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ==================== 参数设定 ====================
K = 97.5           # 行权价
r = 0.043          # 无风险利率 4.3%
T = 0.58           # 剩余期限 0.58 年
S_grid = np.linspace(70, 140, 500)  # 标的价格网格从 70 到 140

# 波动率参数化（可自由调整该列表以观察不同波动率下的 Delta 特征）
volatilities = [0.15, 0.276, 0.40]
vol_labels = ['15%', '27.6%', '40%']

# ==================== 1 & 2. 计算 Delta 并绘图 ====================
plt.figure(figsize=(10, 6))

for sigma, label in zip(volatilities, vol_labels):
    delta_curve = bs_call_delta(S=S_grid, K=K, T=T, r=r, sigma=sigma)
    plt.plot(S_grid, delta_curve, label=f'Vol = {label}', linewidth=2)

# 图表修饰
plt.title('European Call Option Delta vs Underlying Price (Black-Scholes)', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(K, color='gray', linestyle='--', linewidth=0.8, label=f'Strike K={K}')
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# ==================== 3. 报告特定点的 Delta ====================
S_target = 110
vol_target = 0.276
delta_s110 = bs_call_delta(S=S_target, K=K, T=T, r=r, sigma=vol_target)

# 在图中标注该特定点以增强教学展示效果
plt.scatter([S_target], [delta_s110], color='red', zorder=5)
plt.annotate(f'S=110, Vol=27.6%\nDelta={delta_s110:.4f}',
             xy=(S_target, delta_s110),
             xytext=(S_target + 5, delta_s110 - 0.12),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
             fontsize=10)

# ==================== 4. 保存图形并填充 result ====================
figure_path = 'bs_call_delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 将结果存入字典，delta 保留 4 位小数
result = {
    'delta_at_s110': float(round(delta_s110, 4)),
    'figure_path': figure_path
}

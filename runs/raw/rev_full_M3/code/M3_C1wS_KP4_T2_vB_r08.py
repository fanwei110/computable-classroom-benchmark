import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ================= 参数设定 =================
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 到期期限 (年)
S_min = 70        # 标的价格网格下限
S_max = 140       # 标的价格网格上限
vols = [0.15, 0.276, 0.40]  # 三条曲线的波动率

target_S = 110    # 需要报告Delta的标的价格
target_vol = 0.276 # 需要报告Delta的波动率

# ================= 核心计算函数 =================
def bs_call_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes Delta。
    题目未指明看涨/看跌，行业惯例默认为看涨期权 Delta = N(d1)。
    """
    S = np.asarray(S)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ================= 1. 计算网格与目标Delta =================
S_grid = np.linspace(S_min, S_max, 500)
delta_at_s110 = bs_call_delta(target_S, K, T, r, target_vol)

# ================= 2. 绘图 =================
plt.figure(figsize=(10, 6))

# 参数化绘制三条波动率曲线
for sigma in vols:
    deltas = bs_call_delta(S_grid, K, T, r, sigma)
    plt.plot(S_grid, deltas, label=f'vol = {sigma*100:.1f}%', linewidth=2)

# 标记目标点 S=110, vol=27.6% 的位置
plt.scatter([target_S], [delta_at_s110], color='red', zorder=5)
plt.annotate(f'S=110, vol=27.6%\nDelta={delta_at_s110:.4f}',
             xy=(target_S, delta_at_s110),
             xytext=(target_S + 5, delta_at_s110 - 0.15),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
             fontsize=11,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.title('European Call Option Delta vs Underlying Price', fontsize=14)
plt.xlabel('Underlying Asset Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)
plt.axhline(1, color='gray', linestyle='--', linewidth=0.8)
plt.axvline(K, color='green', linestyle=':', linewidth=1, label=f'Strike K = {K}')
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图形
figure_path = 'bs_delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 3. 输出结果 =================
result = {
    'delta_at_s110': float(delta_at_s110),
    'figure_path': figure_path
}

# 打印结果以便课堂展示
print(f"标的110, 波动率27.6%的Delta为: {result['delta_at_s110']:.4f}")
print(f"图形已保存至: {result['figure_path']}")

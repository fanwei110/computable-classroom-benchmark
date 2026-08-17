import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ---------------- 参数设置 ----------------
K = 97.5          # 行权价
r = 0.043         # 利率 4.3%
T = 0.58          # 剩余期限 0.58年
S_range = np.linspace(70, 140, 700)  # 标的价格从70到140

# 可调波动率参数（修改此列表即可调整图中的线条）
volatilities = [0.15, 0.276, 0.40]

# ---------------- 核心计算函数 ----------------
def call_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的Delta
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ---------------- 特定值计算 ----------------
# 报标的等于110、波动率27.6%时的delta
target_S = 110
target_sigma = 0.276
delta_at_s110 = call_delta(target_S, K, T, r, target_sigma)

# ---------------- 绘图 ----------------
plt.figure(figsize=(10, 6))

# 遍历波动率参数画线
for sigma in volatilities:
    deltas = call_delta(S_range, K, T, r, sigma)
    # 图例标好具体的波动率百分比
    plt.plot(S_range, deltas, label=f'Vol = {sigma * 100:.1f}%')

plt.title('Delta vs Underlying Price (Call Option)')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图表
figure_path = 'delta_vs_price.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ---------------- 按契约要求存入字典 ----------------
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以供查验
print(f"标的110、波动率27.6%时的Delta: {result['delta_at_s110']:.4f}")
print(f"图片保存路径: {result['figure_path']}")
print("Result Dictionary:", result)

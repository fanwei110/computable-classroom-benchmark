import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ==================== 参数设定 ====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (年化)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的资产分红率 (题目未指明，假设为0)

# 标的资产价格网格
S_min, S_max = 70, 140
S_grid = np.linspace(S_min, S_max, 500)

# 波动率可调参数 (题目要求的三条曲线)
volatilities = [0.15, 0.276, 0.40]
vol_labels = ['15%', '27.6%', '40%']

# ==================== 核心计算函数 ====================
def bs_call_delta(S, K, T, r, sigma, q=0.0):
    """
    计算欧式看涨期权的 Delta (闭式解)
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = np.exp(-q * T) * norm.cdf(d1)
    return delta

# ==================== 1. 计算每个波动率在标的网格上的 delta ====================
delta_curves = {}
for sigma in volatilities:
    delta_curves[sigma] = bs_call_delta(S_grid, K, T, r, sigma, q)

# ==================== 2. 绘制三条带标注曲线 ====================
plt.figure(figsize=(10, 6))

# 遍历波动率画图
for sigma, label in zip(volatilities, vol_labels):
    plt.plot(S_grid, delta_curves[sigma], label=f'σ = {label}', linewidth=2)

plt.title('European Call Option Delta vs Underlying Price', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.axvline(x=K, color='grey', linestyle='--', linewidth=1, label=f'Strike K = {K}')
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'european_call_delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==================== 3. 报告标的110、波动率27.6%的 delta ====================
S_target = 110
sigma_target = 0.276
delta_at_s110 = bs_call_delta(S_target, K, T, r, sigma_target, q)

# ==================== 4. 填充 result 字典 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 课堂投屏展示结果
print(f"标的价格 S=110, 波动率 σ=27.6% 时的 Delta 为: {delta_at_s110:.6f}")
print(f"图形已保存至: {figure_path}")
print("\nResult Dictionary:")
print(result)

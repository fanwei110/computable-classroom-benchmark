import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# =====================
// 参数设定
# =====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (年化)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 股息率 (标的不分红)

# 标的资产价格网格与波动率参数
S_min, S_max = 70, 140
S_grid = np.linspace(S_min, S_max, 500)
volatilities = [0.15, 0.276, 0.40]  # 波动率参数化列表

# =====================
// Black-Scholes Delta 闭式解
# =====================
def bs_call_delta(S, K, T, r, sigma, q=0.0):
    """
    计算不分红欧式看涨期权的 Delta
    Delta = N(d1)
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# =====================
// 计算并绘图
# =====================
plt.figure(figsize=(10, 6))

# 针对每个波动率计算 delta 并画曲线
for sigma in volatilities:
    deltas = bs_call_delta(S_grid, K, T, r, sigma, q)
    plt.plot(S_grid, deltas, label=f'Vol = {sigma*100:.1f}%')

# 图表格式设置
plt.title('European Call Option Delta vs Underlying Price', fontsize=14)
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# =====================
// 报告特定值
# =====================
S_target = 110
sigma_target = 0.276
delta_at_s110 = bs_call_delta(S_target, K, T, r, sigma_target, q)

# =====================
// 填充输出契约
# =====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以供课堂展示
print(f"当标的价格为 {S_target}，波动率为 {sigma_target*100}% 时，看涨期权 Delta 为: {delta_at_s110:.4f}")
print(f"图形已保存至: {figure_path}")

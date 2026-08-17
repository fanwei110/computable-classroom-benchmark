import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ===================== 参数设定 =====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率 (连续复利)
T = 0.58          # 剩余期限 (年)
q = 0.0           # 标的分红率 (无分红)

# 波动率参数化 (可调)
sigma_list = [0.15, 0.276, 0.40]

# 标的价格网格
S = np.linspace(70, 140, 500)

# ===================== 核心计算函数 =====================
def call_delta(S, K, r, T, sigma, q=0.0):
    """
    计算欧式看涨期权的 Delta (连续复利利率)
    Delta = N(d1)
    d1 = [ln(S/K) + (r - q + 0.5*sigma^2)*T] / (sigma*sqrt(T))
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ===================== 绘图 =====================
plt.figure(figsize=(10, 6))

# 对每个波动率计算并绘制 Delta 曲线
for sigma in sigma_list:
    delta_vals = call_delta(S, K, r, T, sigma, q)
    plt.plot(S, delta_vals, label=f'σ = {sigma*100:.1f}%')

plt.title('European Call Option Delta vs Spot Price', fontsize=14)
plt.xlabel('Spot Price (S)', fontsize=12)
plt.ylabel('Delta (N(d1))', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ===================== 报告特定点的 Delta =====================
S_target = 110
sigma_target = 0.276
delta_at_s110 = call_delta(S_target, K, r, T, sigma_target, q)

# ===================== 输出契约 =====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 打印结果以供验证
print(result)

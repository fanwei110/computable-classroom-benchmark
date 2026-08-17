import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def calculate_call_delta(S, K, r, T, sigma, q=0.0):
    """
    计算欧式看涨期权的 Delta (连续复利)
    Delta = N(d1)
    d1 = [ln(S/K) + (r - q + 0.5 * sigma^2) * T] / (sigma * sqrt(T))
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 课程计算约定参数
K = 97.5        # 行权价
r = 0.043       # 无风险利率 (小数表示)
T = 0.58        # 剩余期限 (年)
q = 0.0         # 标的不分红

# 波动率做成可调参数
sigma_list = [0.15, 0.276, 0.40]

# 标的价格网格
S_grid = np.linspace(70, 140, 500)

# 绘制 Delta 曲线
plt.figure(figsize=(10, 6))
for sigma in sigma_list:
    delta_grid = calculate_call_delta(S_grid, K, r, T, sigma, q)
    plt.plot(S_grid, delta_grid, label=f'Vol = {sigma*100:.1f}%')

plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.title('European Call Option Delta across Different Volatilities')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 计算标的 110、波动率 27.6% 时的 delta
s_target = 110.0
sigma_target = 0.276
delta_at_s110 = calculate_call_delta(s_target, K, r, T, sigma_target, q)

# 构造输出契约字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 验证输出结果（可打印查看）
print(f"Delta at S=110, sigma=27.6%: {result['delta_at_s110']:.6f}")
print(f"Figure saved to: {result['figure_path']}")

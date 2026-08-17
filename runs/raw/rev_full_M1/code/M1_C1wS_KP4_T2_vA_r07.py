import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

# Black-Scholes 欧式看涨期权 delta 计算函数
def black_scholes_call_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 delta
    S: 标的资产价格
    K: 行权价
    T: 剩余到期时间（年）
    r: 无风险利率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# 参数设置
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余到期时间（年）
S_range = np.linspace(70, 140, 100)  # 标的价格范围
volatilities = [0.15, 0.276, 0.40]  # 波动率列表

# 1. 对每个波动率在标的网格上计算 delta
delta_values = {}
for sigma in volatilities:
    delta_values[sigma] = black_scholes_call_delta(S_range, K, T, r, sigma)

# 2. 画三条带标注曲线
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    plt.plot(S_range, delta_values[sigma], label=f'Volatility = {sigma:.1%}')

plt.title('Call Option Delta vs Underlying Price')
plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_vs_underlying.png'
plt.savefig(figure_path)
plt.close()

# 3. 报告标的 110、波动率 27.6% 的 delta
S_target = 110
sigma_target = 0.276
delta_at_s110 = black_scholes_call_delta(S_target, K, T, r, sigma_target)

# 4. 填充 result 字典
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果以供验证
print(result)

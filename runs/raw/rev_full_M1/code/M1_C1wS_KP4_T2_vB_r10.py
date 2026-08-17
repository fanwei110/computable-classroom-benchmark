import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算欧式期权的Black-Scholes Delta
    S: 标的资产价格
    K: 行权价
    T: 到期时间（年）
    r: 无风险利率
    sigma: 波动率
    option_type: 'call'或'put'
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    return delta

# 参数设置
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 到期时间（年）
volatilities = [0.15, 0.276, 0.40]  # 波动率列表
S_range = np.linspace(70, 140, 100)  # 标的价格范围

# 计算不同波动率下的delta曲线
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    deltas = [black_scholes_delta(S, K, T, r, sigma) for S in S_range]
    plt.plot(S_range, deltas, label=f'Vol = {sigma*100:.1f}%')

# 图形设置
plt.title('Black-Scholes Delta for European Call Option')
plt.xlabel('Underlying Asset Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curves.png'
plt.savefig(figure_path)
plt.close()

# 计算特定点的delta值
S_target = 110
sigma_target = 0.276
delta_at_s110 = black_scholes_delta(S_target, K, T, r, sigma_target)

# 准备结果
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供教师查看）
print(result)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算Black-Scholes模型下的Delta值
    S: 标的价格
    K: 行权价
    T: 剩余期限（年）
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
K = 97.5  # 行权价
r = 0.043  # 无风险利率
T = 0.58  # 剩余期限（年）
S_range = np.linspace(70, 140, 100)  # 标的价格范围
volatilities = [0.15, 0.276, 0.40]  # 波动率列表

# 计算不同波动率下的Delta值
deltas = {}
for sigma in volatilities:
    deltas[sigma] = [black_scholes_delta(S, K, T, r, sigma) for S in S_range]

# 绘制图形
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    plt.plot(S_range, deltas[sigma], label=f'Volatility = {sigma*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', label='Strike Price')
plt.title('Delta vs Underlying Price for Different Volatilities')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_vs_underlying.png'
plt.savefig(figure_path)
plt.close()

# 计算S=110, sigma=27.6%时的Delta
S_110 = 110
sigma_276 = 0.276
delta_at_s110 = black_scholes_delta(S_110, K, T, r, sigma_276)

# 存储结果
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

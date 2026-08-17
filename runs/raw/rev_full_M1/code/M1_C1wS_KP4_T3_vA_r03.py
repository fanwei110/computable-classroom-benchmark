import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产价格
K = 97.5           # 行权价
sigma = 0.276      # 波动率 (27.6%)
r = 0.043          # 无风险利率 (4.3%)
T = 0.58           # 剩余期限 (年)
d_sigma = 0.01     # 波动率变化 (1%)

# Black-Scholes 辅助函数
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# 计算 vega (期权价格对波动率的敏感度)
def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T) / 100  # 以百分点为单位

# 计算初始期权价格和 vega
initial_price = black_scholes(S, K, T, r, sigma)
vega_value = vega(S, K, T, r, sigma)

# 计算波动率变化一个百分点时的价格变化
price_change = vega_value * d_sigma * 100  # vega 已经是每 1% 变化的敏感度

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，用于调试）
print(result)

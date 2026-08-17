import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产价格
K = 97.5           # 行权价
sigma = 0.276      # 波动率 (27.6%)
r = 0.043          # 无风险利率 (4.3%)
T = 0.58           # 剩余期限 (年)
sigma_change = 0.01  # 波动率变化 (1%)

# Black-Scholes 欧式期权定价函数
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# 计算 Vega (期权价格对波动率的敏感度)
def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T) / 100  # 除以100将Vega转换为每1%波动率变化的价格变化

# 计算初始期权价格
initial_price = black_scholes(S, K, T, r, sigma)

# 计算Vega
vega_value = vega(S, K, T, r, sigma)

# 计算波动率变化1%时的价格变化
price_change = vega_value * sigma_change * 100  # 乘以100将1%转换为1个百分点

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，用于验证）
print(f"期权价格变化: {price_change:.4f}")

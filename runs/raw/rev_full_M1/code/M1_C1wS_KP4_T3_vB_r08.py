import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（27.6%）
r = 0.043       # 无风险利率（4.3%）
T = 0.58        # 到期时间（0.58年）

# Black-Scholes公式计算欧式期权价格
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# 计算vega（波动率变化1%时的价格变化）
def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) * 0.01  # 乘以0.01将1%转换为小数
    return vega

# 计算初始期权价格（假设为看涨期权）
initial_price = black_scholes(S, K, T, r, sigma, option_type='call')

# 计算vega
vega_value = vega(S, K, T, r, sigma)

# IV增加1个百分点（即0.01）时的价格变化
price_change = vega_value * 1  # 因为vega已经乘以0.01，所以乘以1表示1个百分点

# 存储结果
result = {
    'price_change': price_change
}

print(result)

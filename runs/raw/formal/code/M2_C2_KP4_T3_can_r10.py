import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7       # 标的价格
K = 97.5        # 行权价
sigma = 0.276   # 波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余期限 (年)
dsigma = 0.01   # 波动率上升一个百分点

# Black-Scholes 看涨期权价格公式
def bs_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 计算原波动率和上升后的价格
C_old = bs_call_price(S, K, T, r, sigma)
C_new = bs_call_price(S, K, T, r, sigma + dsigma)

# 价格变化
price_change = C_new - C_old

# 保存结果
result = {'price_change': price_change}

# 输出结果供检查
print(result)

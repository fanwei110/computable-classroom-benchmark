import numpy as np
from scipy.stats import norm

def bs_call_price(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格
    S: 标的资产现价
    K: 行权价
    T: 剩余到期时间（年）
    r: 无风险利率（连续复利）
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 给定参数
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
T = 0.58        # 剩余到期时间
r = 0.043       # 无风险利率 (4.3%)
sigma_base = 0.276  # 基础波动率 (27.6%)
sigma_up = 0.286    # 上升一个百分点后的波动率 (28.6%)

# 1. 分别在波动率 28.6% 与 27.6% 下精确重定价
price_base = bs_call_price(S, K, T, r, sigma_base)
price_up = bs_call_price(S, K, T, r, sigma_up)

# 2. 精确价差
price_change = price_up - price_base

# 按照输出契约存入字典
result = {'price_change': price_change}

# 打印结果以便验证
print(result)

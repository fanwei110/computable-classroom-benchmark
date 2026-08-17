import numpy as np
from scipy.stats import norm

# 输入参数
S0 = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58
q = 0.0  # 不分红

# 计算 d1 和 d2
d1 = (np.log(S0 / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 看涨期权价格
call_price = S0 * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = np.exp(-q * T) * norm.cdf(d1)

# Vega (每 1% 波动率变化对应的价格变化)
call_vega = S0 * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1) * 0.01

# 结果存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

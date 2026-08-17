import numpy as np
from scipy.stats import norm

# 参数
S0 = 103.7
K = 97.5
sigma = 0.276
r_annual = 0.043
r = np.log(1 + r_annual)  # 连续复利
T = 0.58

# 计算 d1 和 d2
d1 = (np.log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算期权价格
call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算 Delta
call_delta = norm.cdf(d1)

# 计算 Vega
call_vega = S0 * np.sqrt(T) * norm.pdf(d1)

# 存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

result

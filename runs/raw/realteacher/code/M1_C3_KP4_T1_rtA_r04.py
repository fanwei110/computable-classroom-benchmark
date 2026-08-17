import numpy as np
from scipy.stats import norm

# 参数
S = 103.7
K = 97.5
sigma = 0.276
r = np.log(1 + 0.043)  # 连续复利
T = 0.58

# 计算d1和d2
d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算Delta
call_delta = norm.cdf(d1)

# 计算Vega
call_vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # 通常Vega表示波动率变化1%时的价格变化

# 存入结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58

# 计算d1和d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算Delta
call_delta = norm.cdf(d1)

# 计算Vega（每1%波动率变化）
call_vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01

# 存入结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

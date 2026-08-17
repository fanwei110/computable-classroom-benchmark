import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7       # 标的现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率
r = 0.043       # 无风险利率
T = 0.58        # 剩余到期时间

# Black-Scholes 公式
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * np.sqrt(T) * norm.pdf(d1)  # Vega 定义为对波动率（小数形式）的偏导数

result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print(result)

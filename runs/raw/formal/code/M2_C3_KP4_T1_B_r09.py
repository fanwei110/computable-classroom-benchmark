import numpy as np
from scipy.stats import norm

S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58

d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

result = {
    'call_price': round(call_price, 6),
    'call_delta': round(call_delta, 6),
    'call_vega': round(call_vega, 6)
}

# 按指定精度输出
print(result)

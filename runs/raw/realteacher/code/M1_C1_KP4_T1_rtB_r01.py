import numpy as np
from scipy.stats import norm

def black_scholes_call(S, X, T, r, sigma):
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)
    call_delta = norm.cdf(d1)
    call_vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # Vega通常以1%波动率变化为单位

    return call_price, call_delta, call_vega

# 输入参数
S = 103.7
X = 97.5
T = 0.58
r = 0.043
sigma = 0.276

# 计算
call_price, call_delta, call_vega = black_scholes_call(S, X, T, r, sigma)

# 存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    call_delta = np.exp(-q * T) * norm.cdf(d1)
    call_vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1) * 0.01  # 每 1% 波动率变化

    return call_price, call_delta, call_vega

# 输入参数
S = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276
q = 0

# 计算
call_price, call_delta, call_vega = black_scholes_call(S, K, T, r, sigma, q)

# 存入 result 字典
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print(result)

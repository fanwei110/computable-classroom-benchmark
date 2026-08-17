import numpy as np
from scipy.stats import norm
from math import log, sqrt, exp

# 输入参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（年化）
r = 0.043          # 无风险利率（年化）
T = 0.58           # 剩余期限（年）

# Black-Scholes 公式辅助函数
def black_scholes_call(S, K, T, r, sigma):
    d1 = (log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    call_price = S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    call_delta = norm.cdf(d1)
    call_vega = S * sqrt(T) * norm.pdf(d1) * 0.01  # Vega 通常以 1% 波动率变化为单位
    return call_price, call_delta, call_vega

# 计算期权价格、Delta 和 Vega
call_price, call_delta, call_vega = black_scholes_call(S, K, T, r, sigma)

# 存储结果
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（可选，用于验证）
print(result)

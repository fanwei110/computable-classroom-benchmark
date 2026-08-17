import math
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    # S: 标的现价
    # K: 行权价
    # T: 剩余到期时间（年）
    # r: 无风险利率
    # sigma: 隐含波动率

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    call_delta = norm.cdf(d1)
    call_vega = S * math.sqrt(T) * norm.pdf(d1) * 0.01  # Vega通常表示为波动率变化1%时的价格变化

    return call_price, call_delta, call_vega

# 输入参数
S = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276

# 计算
call_price, call_delta, call_vega = black_scholes_call(S, K, T, r, sigma)

# 存入结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

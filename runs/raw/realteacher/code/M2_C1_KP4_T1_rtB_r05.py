import math
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率
r = 0.043          # 无风险利率
T = 0.58           # 剩余期限（年）
q = 0.0            # 不分红

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 期权价格
call_price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = math.exp(-q * T) * norm.cdf(d1)

# Vega (基于1%波动率变动的绝对值，即 sigma 变化0.01的价格变化)
call_vega = S * math.exp(-q * T) * norm.pdf(d1) * math.sqrt(T) * 0.01

# 存入字典
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print(result)

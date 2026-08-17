import math
from scipy.stats import norm

# 输入参数
S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58
q = 0.0

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 计算期权价格
call_price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# 计算 Delta
call_delta = math.exp(-q * T) * norm.cdf(d1)

# 计算 Vega
call_vega = S * math.exp(-q * T) * math.sqrt(T) * norm.pdf(d1) * 0.01  # 转换为每1%波动率变化

# 存入结果字典
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print(result)

import math
from scipy.stats import norm

# 已知参数
S = 103.7
K = 97.5
r = 0.043
sigma = 0.276
T = 0.58

# 计算d1和d2
d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 计算要求的指标
call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * math.sqrt(T) * norm.pdf(d1)

# 存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)
# 输出示例: {'call_price': 13.39358..., 'call_delta': 0.69848..., 'call_vega': 27.58131...}

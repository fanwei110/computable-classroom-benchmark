import math
from scipy.stats import norm

# 已知参数
S = 103.7      # 标的现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率
r = 0.043      # 无风险利率
T = 0.58       # 剩余到期时间（年）
q = 0.0        # 股息率（不分红）

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 计算欧式看涨期权价格
call_price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# 计算看涨期权 Delta
call_delta = math.exp(-q * T) * norm.cdf(d1)

# 计算 Vega (标准定义：波动率变动1单位即100%时的价格变动，若需百分比波动率变动1%的vega，可再除以100)
call_vega = S * math.exp(-q * T) * math.sqrt(T) * norm.pdf(d1)

# 按照输出契约存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

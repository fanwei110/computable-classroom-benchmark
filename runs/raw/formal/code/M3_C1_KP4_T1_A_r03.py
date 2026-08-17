import math
from scipy.stats import norm

# 给定参数
S = 103.7      # 标的现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率
r = 0.043      # 无风险利率
T = 0.58       # 剩余到期时间（年）

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 计算看涨期权价格
call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# 计算 Delta
call_delta = norm.cdf(d1)

# 计算 Vega (通常Vega按1单位波动率变动计算，即绝对值；若按1%变动则需除以100，此处按标准绝对导数输出)
call_vega = S * norm.pdf(d1) * math.sqrt(T)

# 按照输出契约存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

result

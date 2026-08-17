import math
from scipy.stats import norm

# 给定参数
S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率（小数形式）
r = 0.043        # 无风险利率
T = 0.58         # 到期时间（年）

# 计算d1和d2
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 期权价格
call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = norm.cdf(d1)

# Vega（对波动率σ的偏导数，σ以小数表示）
call_vega = S * math.sqrt(T) * norm.pdf(d1)

# 输出结果
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

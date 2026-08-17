import math
from scipy.stats import norm

# 给定参数
S = 103.7           # 标的现价
K = 97.5            # 行权价
sigma = 0.276       # 隐含波动率（小数）
r = 0.043           # 无风险利率（连续复利，小数）
T = 0.58            # 剩余到期时间（年）
q = 0.0             # 不分红

# 计算 d1, d2
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 计算价格、delta、vega
call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * norm.pdf(d1) * math.sqrt(T)   # 对波动率（小数）的导数

# 存入字典
result = {
    'call_price': round(call_price, 6),
    'call_delta': round(call_delta, 6),
    'call_vega': round(call_vega, 6)
}

# 输出结果
print(result)

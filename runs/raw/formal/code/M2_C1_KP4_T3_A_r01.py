import math

S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58

# 计算 d1
d1 = (math.log(S/K) + (r + sigma**2/2)*T) / (sigma * math.sqrt(T))
# 计算 N'(d1)
nd1 = math.exp(-d1**2/2) / math.sqrt(2 * math.pi)
# 计算 Vega（波动率每变动1，即100个百分点，期权价格的变动）
vega = S * math.sqrt(T) * nd1
# 隐含波动率涨1个百分点（0.01）带来期权价格的变化
price_change = vega * 0.01

result = {'price_change': round(price_change, 4)}
print(result)

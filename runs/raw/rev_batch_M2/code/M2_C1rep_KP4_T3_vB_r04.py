import math

# 给定参数
S = 103.7      # 标的现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率
r = 0.043      # 无风险利率
T = 0.58       # 到期时间

# 计算 d1
d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
# 标准正态分布概率密度函数 N'(d1)
nd1 = math.exp(-0.5 * d1**2) / math.sqrt(2 * math.pi)
# Vega（波动率变化1单位，即100%的价格变化）
vega = S * math.sqrt(T) * nd1
# IV上涨1个百分点（0.01）的价格变化
price_change = vega * 0.01

result = {'price_change': round(price_change, 4)}
result

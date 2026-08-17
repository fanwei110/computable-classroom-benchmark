import math

# 给定参数
S = 103.7      # 标的价格
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率
r = 0.043      # 无风险利率
T = 0.58       # 到期年限

# 计算 d1
d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
# 计算标准正态分布概率密度函数 N'(d1)
nd1 = math.exp(-d1**2 / 2) / math.sqrt(2 * math.pi)
# 计算 Vega (波动率每变动 1 单位，即 100 个百分点，对应的期权价格变化)
vega = S * math.sqrt(T) * nd1
# IV 涨 1 个点 = 0.01，因此价格变动 = vega * 0.01
price_change = vega * 0.01

result = {'price_change': round(price_change, 6)}
result

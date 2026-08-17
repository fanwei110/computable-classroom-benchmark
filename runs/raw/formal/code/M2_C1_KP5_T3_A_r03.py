import math

# 给定参数
sigma_annual = 0.24          # 年化波动率
position = 2700000.0         # 头寸（元）
z_95 = 1.6448536269514722   # 95%置信水平下的标准正态分位数

# 将年化波动率转换为日波动率（假设一年252个交易日）
sigma_daily = sigma_annual / math.sqrt(252)

# 计算一日VaR
var_95_1d = position * sigma_daily * z_95

# 结果保留两位小数
result = {'var_95_1d': round(var_95_1d, 2)}
result

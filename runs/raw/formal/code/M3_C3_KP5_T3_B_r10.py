import math

# 已知参数
vol_annual = 0.24
position = 2700000
z_95 = 1.6448536269514777  # 95%正态分布分位数

# 计算日波动率
vol_daily = vol_annual / math.sqrt(252)

# 计算95%一日VaR
var_95_1d = z_95 * vol_daily * position

# 存入字典
result = {'var_95_1d': round(var_95_1d, 2)}

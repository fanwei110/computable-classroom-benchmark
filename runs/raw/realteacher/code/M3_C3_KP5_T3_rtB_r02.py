import math

# 已知参数
sigma_annual = 0.24
position = 2700000
trading_days = 252
z_95 = 1.644853  # 95%置信区间的标准正态分位数

# 计算日波动率
sigma_daily = sigma_annual / math.sqrt(trading_days)

# 计算95%一日VaR
var_95_1d = position * z_95 * sigma_daily

result = {'var_95_1d': round(var_95_1d, 2)}

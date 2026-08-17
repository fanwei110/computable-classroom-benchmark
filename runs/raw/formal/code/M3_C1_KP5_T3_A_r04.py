import math

# 已知参数
annual_volatility = 0.24
position = 2700000
z_95 = 1.645  # 95%置信度对应的正态分布分位数
trading_days = 252  # 假设一年252个交易日

# 计算日波动率
daily_volatility = annual_volatility / math.sqrt(trading_days)

# 计算95%一日VaR
var_95_1d = position * z_95 * daily_volatility

# 按照输出契约存入字典
result = {'var_95_1d': var_95_1d}

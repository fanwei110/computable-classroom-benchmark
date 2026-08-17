import math

# 给定参数
annual_volatility = 0.24
position_value = 2700000  # 元
confidence_level = 0.95
trading_days = 252  # 通常假设一年252个交易日

# 计算日波动率
daily_volatility = annual_volatility / math.sqrt(trading_days)

# 95%置信水平对应的标准正态分布分位数（单尾）
z_score = 1.6448536269514722

# 计算1日VaR
var_95_1d = position_value * daily_volatility * z_score

# 结果存入字典
result = {'var_95_1d': var_95_1d}

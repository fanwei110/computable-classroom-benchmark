import math

# 输入参数
annual_vol = 0.24
position = 2_700_000
confidence_z = 1.645  # 95% 单尾正态分布分位数
trading_days = 252  # 假设一年252个交易日

# 计算一日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 计算VaR
var_95_1d = position * daily_vol * confidence_z

# 输出结果字典
result = {'var_95_1d': round(var_95_1d, 2)}

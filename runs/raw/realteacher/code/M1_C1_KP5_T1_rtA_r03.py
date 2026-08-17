import math

# 输入参数
position = 1850000
annual_volatility = 0.218
days_in_year = 252

# 计算一天的波动率
daily_volatility = annual_volatility / math.sqrt(days_in_year)

# 95% 一天的 VaR
z_95 = 1.645
var_95_1d = position * z_95 * daily_volatility

# 计算十天的波动率
ten_day_volatility = daily_volatility * math.sqrt(10)

# 99% 十天的 VaR
z_99 = 2.326
var_99_10d = position * z_99 * ten_day_volatility

# 存入字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

result

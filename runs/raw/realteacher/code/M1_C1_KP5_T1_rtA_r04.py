import math

# 输入参数
position = 1850000  # 头寸
annual_volatility = 0.218  # 年化波动率
trading_days_per_year = 252  # 一年的交易日数

# 计算一天的波动率
daily_volatility = annual_volatility / math.sqrt(trading_days_per_year)

# 95%置信水平下一天的VaR
z_95 = 1.645
var_95_1d = position * z_95 * daily_volatility

# 计算十天的波动率
ten_day_volatility = daily_volatility * math.sqrt(10)

# 99%置信水平下十天的VaR
z_99 = 2.326
var_99_10d = position * z_99 * ten_day_volatility

# 存入结果字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

print(result)

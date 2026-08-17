import math

# 输入参数
position = 1850000  # 头寸185万元
annual_volatility = 0.218  # 年化波动率21.8%

# 计算一日波动率
daily_volatility = annual_volatility / math.sqrt(252)

# 95%置信水平的一日VaR
z_95 = 1.645
var_95_1d = position * z_95 * daily_volatility

# 99%置信水平的十日VaR
z_99 = 2.326
ten_day_volatility = daily_volatility * math.sqrt(10)
var_99_10d = position * z_99 * ten_day_volatility

# 结果存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

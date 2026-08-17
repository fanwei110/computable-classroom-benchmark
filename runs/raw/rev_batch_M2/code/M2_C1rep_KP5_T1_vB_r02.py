import math

# 给定参数
position = 1850000
annual_vol = 0.218
days_per_year = 252

# 置信水平对应的z值（单尾）
z_95 = 1.645   # 95%
z_99 = 2.326   # 99%

# 计算日波动率与十日波动率
daily_vol = annual_vol / math.sqrt(days_per_year)
ten_day_vol = annual_vol * math.sqrt(10 / days_per_year)

# 参数法 VaR
var_95_1d = position * z_95 * daily_vol
var_99_10d = position * z_99 * ten_day_vol

# 按要求存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

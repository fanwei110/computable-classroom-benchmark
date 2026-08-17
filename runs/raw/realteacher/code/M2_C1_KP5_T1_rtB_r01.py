import math

# 给定参数
position = 185  # 单位：万元
annual_vol = 0.218
trading_days = 252

# 日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 十日波动率
ten_day_vol = annual_vol * math.sqrt(10 / trading_days)

# Z 值 (95% 和 99% 置信水平下的单尾临界值)
z_95 = 1.645
z_99 = 2.326

# VaR 计算
var_95_1d = position * daily_vol * z_95
var_99_10d = position * ten_day_vol * z_99

# 结果存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

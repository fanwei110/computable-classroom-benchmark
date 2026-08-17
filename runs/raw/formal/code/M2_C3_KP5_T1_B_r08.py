import math

# 给定参数
position = 1850000  # 仓位
annual_vol = 0.218  # 年化波动率
trading_days = 252

# 分位数
z_95 = 1.6448536269514722   # 95% 单尾
z_99 = 2.3263478740408408   # 99% 单尾

# 日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 10天波动率
ten_day_vol = annual_vol * math.sqrt(10 / trading_days)

# VaR 计算
var_95_1d = position * daily_vol * z_95
var_99_10d = position * ten_day_vol * z_99

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}
result

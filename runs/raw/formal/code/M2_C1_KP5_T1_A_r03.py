import math
from scipy.stats import norm

# 参数设置
position = 1_850_000  # 头寸 185 万元
annual_vol = 0.218    # 年化波动率
trading_days = 252

# 日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# z 值
z_95 = norm.ppf(0.95)  # 1.6448536269514722
z_99 = norm.ppf(0.99)  # 2.3263478740408408

# 1日 VaR (95% 置信)
var_95_1d = position * daily_vol * z_95

# 10日 VaR (99% 置信)
ten_day_vol = daily_vol * math.sqrt(10)
var_99_10d = position * ten_day_vol * z_99

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

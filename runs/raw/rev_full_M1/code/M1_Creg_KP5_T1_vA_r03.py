import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化收益波动率

# 计算参数
confidence_95 = 0.95
confidence_99 = 0.99
z_95 = norm.ppf(confidence_95)  # 95% 置信水平的 Z 值
z_99 = norm.ppf(confidence_99)  # 99% 置信水平的 Z 值

# 时间调整（日波动率 = 年波动率 / sqrt(252)）
trading_days_per_year = 252
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# (i) 95% 一日 VaR
var_95_1d = position_value * z_95 * daily_volatility

# (ii) 99% 十日 VaR（时间调整：sqrt(10)）
ten_day_volatility = daily_volatility * np.sqrt(10)
var_99_10d = position_value * z_99 * ten_day_volatility

# 结果存储
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

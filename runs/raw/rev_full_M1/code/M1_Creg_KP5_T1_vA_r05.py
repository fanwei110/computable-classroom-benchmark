import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化收益波动率（21.8%）

# 常数
days_in_year = 252         # 交易日天数（通常假设一年有252个交易日）
confidence_95 = 0.95       # 95%置信水平
confidence_99 = 0.99       # 99%置信水平

# 计算Z值（标准正态分布的分位数）
z_95 = norm.ppf(confidence_95)
z_99 = norm.ppf(confidence_99)

# 计算一日收益波动率（年化波动率转换为日波动率）
daily_volatility = annual_volatility / np.sqrt(days_in_year)

# 计算95%置信水平下的1日VaR
var_95_1d = position_value * z_95 * daily_volatility

# 计算99%置信水平下的10日VaR（使用平方根法则调整时间）
ten_day_volatility = daily_volatility * np.sqrt(10)
var_99_10d = position_value * z_99 * ten_day_volatility

# 结果存储
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

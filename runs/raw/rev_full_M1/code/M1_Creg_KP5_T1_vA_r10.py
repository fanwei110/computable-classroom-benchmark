import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化收益波动率（21.8%）

# 常数
days_in_year = 252         # 交易日天数（通常假设一年有252个交易日）

# 计算每日波动率
daily_volatility = annual_volatility / np.sqrt(days_in_year)

# (i) 计算95%置信水平下的1日VaR
confidence_level_95 = 0.95
z_score_95 = norm.ppf(confidence_level_95)
var_95_1d = position_value * daily_volatility * z_score_95

# (ii) 计算99%置信水平下的10日VaR
confidence_level_99 = 0.99
z_score_99 = norm.ppf(confidence_level_99)
ten_day_volatility = daily_volatility * np.sqrt(10)  # 10日波动率
var_99_10d = position_value * ten_day_volatility * z_score_99

# 结果存储
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

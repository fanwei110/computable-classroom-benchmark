import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化收益波动率

# 计算参数
confidence_95 = 0.95
confidence_99 = 0.99
days_in_year = 252         # 交易日天数（常用假设）

# 计算一日 VaR (95% 置信水平)
z_score_95 = norm.ppf(confidence_95)
daily_volatility = annual_volatility / np.sqrt(days_in_year)
var_95_1d = position_value * z_score_95 * daily_volatility

# 计算十日 VaR (99% 置信水平)
z_score_99 = norm.ppf(confidence_99)
ten_day_volatility = annual_volatility * np.sqrt(10 / days_in_year)
var_99_10d = position_value * z_score_99 * ten_day_volatility

# 结果存储
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000          # 头寸价值（元）
annual_volatility = 0.218           # 年化波动率（小数）
trading_days_per_year = 252         # 每年交易日数

# 1. 去年化一日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 单尾正态分位数（均值=0）
z_95 = norm.ppf(0.95)               # 95% 置信水平
z_99 = norm.ppf(0.99)               # 99% 置信水平

# 3. 计算 VaR
var_95_1d = position_value * daily_volatility * z_95
var_99_10d = position_value * daily_volatility * np.sqrt(10) * z_99

# 4. 结果存入字典（金额取正值）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

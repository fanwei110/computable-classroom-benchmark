import numpy as np
from scipy.stats import norm

# 给定参数
head = 185  # 头寸（万元）
annual_vol = 0.218  # 年化波动率
trading_days = 252  # 一年交易日

# 置信水平对应的Z值（正态分布单尾分位数）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# 一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# VaR 95% 1日
var_95_1d = head * daily_vol * z_95

# 十日波动率
ten_day_vol = annual_vol * np.sqrt(10 / trading_days)

# VaR 99% 10日
var_99_10d = head * ten_day_vol * z_99

# 结果存入字典，保留两位小数（万元）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

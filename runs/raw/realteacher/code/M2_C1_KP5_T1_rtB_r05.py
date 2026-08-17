import numpy as np
from scipy.stats import norm

# 给定参数
position = 1_850_000       # 头寸185万
sigma_annual = 0.218       # 年化波动率
trading_days = 252         # 假设一年252个交易日

# 计算日波动率和十日波动率
sigma_daily = sigma_annual / np.sqrt(trading_days)
sigma_10d = sigma_annual * np.sqrt(10 / trading_days)

# 计算分位数
z_95 = norm.ppf(0.95)      # 95%置信水平单尾
z_99 = norm.ppf(0.99)      # 99%置信水平单尾

# 计算VaR
var_95_1d = position * sigma_daily * z_95
var_99_10d = position * sigma_10d * z_99

# 存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

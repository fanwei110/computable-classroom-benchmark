import numpy as np
from scipy.stats import norm

# 输入参数
V = 1_850_000
sigma_annual = 0.218
days_per_year = 252

# 95% 一日 VaR
z_95 = norm.ppf(0.95)
sigma_daily = sigma_annual / np.sqrt(days_per_year)
var_95_1d = V * z_95 * sigma_daily

# 99% 十日 VaR
z_99 = norm.ppf(0.99)
sigma_10d = sigma_annual * np.sqrt(10 / days_per_year)
var_99_10d = V * z_99 * sigma_10d

# 结果存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

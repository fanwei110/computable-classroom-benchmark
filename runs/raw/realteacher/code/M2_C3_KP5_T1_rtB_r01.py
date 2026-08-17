import math
from scipy.stats import norm

value = 1850000
sigma_annual = 0.218
days = 252

# 波动率缩放
sigma_d = sigma_annual / math.sqrt(days)
sigma_10 = sigma_annual * math.sqrt(10 / days)

# 分位数
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# VaR（正损失）
var_95_1d = value * sigma_d * z_95
var_99_10d = value * sigma_10 * z_99

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

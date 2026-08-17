import math
from scipy.stats import norm

# 给定参数
head = 1_850_000          # 头寸
sigma_annual = 0.218      # 年化波动率
days_per_year = 252       # 每年交易日

# 分位数
z_95 = norm.ppf(0.95)     # 1.6448536269514722
z_99 = norm.ppf(0.99)     # 2.3263478740408408

# VaR 计算
var_95_1d = head * z_95 * sigma_annual * math.sqrt(1 / days_per_year)
var_99_10d = head * z_99 * sigma_annual * math.sqrt(10 / days_per_year)

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

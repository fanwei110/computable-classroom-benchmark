import math

position = 1_850_000
sigma_annual = 0.218
days = 252
sigma_daily = sigma_annual / math.sqrt(days)

# 正态分布分位数
z_95 = 1.6448536269514722   # scipy.stats.norm.ppf(0.95)
z_99 = 2.3263478740408408   # scipy.stats.norm.ppf(0.99)

var_95_1d = position * sigma_daily * z_95
var_99_10d = position * sigma_daily * math.sqrt(10) * z_99

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

import math

# 给定参数
position = 1850000       # 仓位
vol_annual = 0.218       # 年化波动率

# 置信水平对应的标准正态分位数
z_95 = 1.6448536269514722   # 95%
z_99 = 2.3263478740408408   # 99%

# 1天波动率 (假设一年252个交易日)
sigma_1d = vol_annual / math.sqrt(252)
var_95_1d = position * z_95 * sigma_1d

# 10天波动率
sigma_10d = vol_annual * math.sqrt(10 / 252)
var_99_10d = position * z_99 * sigma_10d

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

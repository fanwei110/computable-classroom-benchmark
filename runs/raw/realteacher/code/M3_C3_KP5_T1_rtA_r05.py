import math

position = 1850000
vol_annual = 0.218
trading_days = 252

# 标准正态分布单侧分位数
z_95 = 1.6448536269514722
z_99 = 2.3263478740408408

# 波动率换算
vol_1d = vol_annual / math.sqrt(trading_days)
vol_10d = vol_1d * math.sqrt(10)

# 计算 VaR
var_95_1d = position * vol_1d * z_95
var_99_10d = position * vol_10d * z_99

# 存入字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

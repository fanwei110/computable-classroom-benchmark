import math

sigma_annual = 0.24
position = 2_700_000
trading_days = 252
z_95 = 1.6448536269514722  # 标准正态95%分位数

sigma_daily = sigma_annual / math.sqrt(trading_days)
var_95_1d = position * sigma_daily * z_95

result = {
    'var_95_1d': round(var_95_1d, 2)  # 以元为单位，保留两位小数
}

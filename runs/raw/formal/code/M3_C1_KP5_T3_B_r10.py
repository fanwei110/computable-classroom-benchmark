import math

# 已知参数
vol_annual = 0.24
position = 2700000
z_95 = 1.645  # 95%置信度对应的正态分布分位数
trading_days = 252  # 假设一年252个交易日

# 计算日波动率
vol_daily = vol_annual / math.sqrt(trading_days)

# 计算 95% 1日 VaR
var_95_1d = z_95 * vol_daily * position

# 按照输出契约存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2)
}

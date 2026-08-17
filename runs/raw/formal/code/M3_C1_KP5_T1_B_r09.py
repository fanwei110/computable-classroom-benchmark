import math

# 输入参数
position = 1850000  # 仓位：185万
vol_annual = 0.218  # 年化波动率：21.8%
trading_days = 252  # 假设一年252个交易日

# 分位数（Z值）
z_95 = 1.6449  # 95%置信度
z_99 = 2.3263  # 99%置信度

# 1. 计算95% 1天VaR
vol_daily = vol_annual / math.sqrt(trading_days)
var_95_1d = position * z_95 * vol_daily

# 2. 计算99% 10天VaR
vol_10d = vol_annual / math.sqrt(trading_days / 10)
var_99_10d = position * z_99 * vol_10d

# 按照输出契约存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

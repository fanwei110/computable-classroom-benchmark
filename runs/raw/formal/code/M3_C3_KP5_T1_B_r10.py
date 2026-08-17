import math
from scipy.stats import norm

# 参数设定
V = 1850000
vol_annual = 0.218
trading_days = 252

# 计算波动率
vol_daily = vol_annual / math.sqrt(trading_days)
vol_10d = vol_daily * math.sqrt(10)

# 计算Z分位数
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# 计算VaR
var_95_1d = V * z_95 * vol_daily
var_99_10d = V * z_99 * vol_10d

# 按照输出契约格式输出，保留两位小数符合金额习惯
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

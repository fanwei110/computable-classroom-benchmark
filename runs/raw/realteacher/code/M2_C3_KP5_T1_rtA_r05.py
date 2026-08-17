import math
from scipy.stats import norm

# 给定参数
position = 1_850_000      # 头寸
sigma_annual = 0.218      # 年化波动率
trading_days = 252        # 每年交易日

# 标准正态分位数
z_95 = norm.ppf(0.95)     # 1.64485363
z_99 = norm.ppf(0.99)     # 2.32634787

# 计算
var_95_1d = position * sigma_annual * z_95 * math.sqrt(1 / trading_days)
var_99_10d = position * sigma_annual * z_99 * math.sqrt(10 / trading_days)

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

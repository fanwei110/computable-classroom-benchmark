import math
from scipy.stats import norm

# 参数
position = 1_850_000         # 头寸185万
sigma_annual = 0.218         # 年化波动率
trading_days = 252           # 一年交易日数

# 计算日波动率
sigma_daily = sigma_annual / math.sqrt(trading_days)

# 分位数
z_95 = norm.ppf(0.95)        # 95%置信度对应的z值
z_99 = norm.ppf(0.99)        # 99%置信度对应的z值

# VaR计算
var_95_1d = position * sigma_daily * z_95
var_99_10d = position * sigma_daily * z_99 * math.sqrt(10)

# 存入字典并保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

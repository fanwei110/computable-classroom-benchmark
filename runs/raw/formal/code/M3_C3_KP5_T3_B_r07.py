import math
from scipy.stats import norm

# 已知参数
V = 2700000
vol_annual = 0.24
trading_days = 252
z_95 = norm.ppf(0.95) # 1.6448536269514739

# 计算日波动率
vol_daily = vol_annual / math.sqrt(trading_days)

# 计算 95% 一日 VaR
var_95_1d = V * vol_daily * z_95

# 按照输出契约存入字典
result = {'var_95_1d': var_95_1d}

import math

# 已知参数
sigma_annual = 0.24
position_value = 2700000
trading_days = 252
z_95 = 1.644853626951  # norm.ppf(0.95)

# 计算日波动率
sigma_daily = sigma_annual / math.sqrt(trading_days)

# 计算 95% 1日 VaR
var_95_1d = position_value * z_95 * sigma_daily

# 输出结果
result = {'var_95_1d': round(var_95_1d, 2)}

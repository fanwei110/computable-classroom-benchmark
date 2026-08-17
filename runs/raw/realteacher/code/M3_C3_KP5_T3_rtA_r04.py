import math

# 已知参数
sigma_annual = 0.24
position = 2700000
z_95 = 1.6448536269514729  # norm.ppf(0.95)

# 计算日波动率
sigma_daily = sigma_annual / math.sqrt(252)

# 计算 95% 一日 VaR
var_95_1d = position * z_95 * sigma_daily

# 按照输出契约存入字典
result = {'var_95_1d': round(var_95_1d, 2)}

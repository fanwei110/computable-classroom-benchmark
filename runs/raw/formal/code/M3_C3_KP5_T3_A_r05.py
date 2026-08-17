import math

# 给定参数
sigma_annual = 0.24
position = 270  # 万元
z_95 = 1.6448536269514729  # norm.ppf(0.95)
trading_days = 252

# 计算日波动率
sigma_daily = sigma_annual / math.sqrt(trading_days)

# 计算 95% 一日 VaR (单位：万元)
var_95_1d = position * z_95 * sigma_daily

# 如果需要以元为单位，可乘以 10000
# var_95_1d = var_95_1d * 10000

result = {
    'var_95_1d': var_95_1d  # 结果约为 6.71382705 (万元) 或 67138.27 (元)
}

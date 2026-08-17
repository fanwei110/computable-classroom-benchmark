import math

# 参数
P = 1_850_000        # 头寸
sigma = 0.218        # 年化波动率
z_95 = 1.64485       # 95%单尾正态分位点
z_99 = 2.32635       # 99%单尾正态分位点
days_per_year = 252  # 通常交易日

# 计算VaR
var_95_1d = P * z_95 * sigma * math.sqrt(1 / days_per_year)
var_99_10d = P * z_99 * sigma * math.sqrt(10 / days_per_year)

# 保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

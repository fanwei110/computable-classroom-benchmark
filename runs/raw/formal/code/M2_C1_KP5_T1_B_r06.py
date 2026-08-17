import math

# 给定参数
position = 1850000  # 仓位185万
annual_vol = 0.218  # 年化波动率
days_per_year = 252  # 假设252个交易日

# 单日波动率
sigma_1d = annual_vol / math.sqrt(days_per_year)

# 10日波动率
sigma_10d = annual_vol * math.sqrt(10 / days_per_year)

# z值（正态分布分位数）
z_95 = 1.6448536   # 95%单尾
z_99 = 2.3263479   # 99%单尾

# 参数法VaR = 仓位 × z × 波动率
var_95_1d = position * z_95 * sigma_1d
var_99_10d = position * z_99 * sigma_10d

# 按要求存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

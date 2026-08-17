import math

# 给定参数
position = 1850000  # 仓位
annual_vol = 0.218  # 年化波动率
days_per_year = 252  # 一年的交易日数

# 标准正态分布分位数
z_95 = 1.64485362695147  # 95% 单尾
z_99 = 2.32634787404084  # 99% 单尾

# 1天波动率
sigma_1d = annual_vol / math.sqrt(days_per_year)
# 10天波动率
sigma_10d = annual_vol * math.sqrt(10 / days_per_year)

# 计算 VaR
var_95_1d = position * sigma_1d * z_95
var_99_10d = position * sigma_10d * z_99

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

import math

position = 185  # 头寸（万元）
annual_vol = 0.218  # 年化波动率

# 95%置信水平的一日VaR
z_95 = 1.645
var_95_1d = position * z_95 * annual_vol * math.sqrt(1/252)

# 99%置信水平的十日VaR
z_99 = 2.326
var_99_10d = position * z_99 * annual_vol * math.sqrt(10/252)

result = {
    'var_95_1d': round(var_95_1d, 4),
    'var_99_10d': round(var_99_10d, 4)
}

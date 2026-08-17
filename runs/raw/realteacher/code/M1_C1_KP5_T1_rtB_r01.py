import math

position = 1850000
annual_vol = 0.218

# 95% 一日VaR
z_95 = 1.645
var_95_1d = position * z_95 * annual_vol * math.sqrt(1 / 252)

# 99% 十日VaR
z_99 = 2.326
var_99_10d = position * z_99 * annual_vol * math.sqrt(10 / 252)

result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

print(result)

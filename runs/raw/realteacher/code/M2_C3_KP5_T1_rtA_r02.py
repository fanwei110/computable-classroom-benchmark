import math

position = 1850000
sigma_annual = 0.218
sqrt_252 = math.sqrt(252)

sigma_1d = sigma_annual / sqrt_252
sigma_10d = sigma_annual * math.sqrt(10 / 252)

z_95 = 1.6448536269514722   # norm.ppf(0.95)
z_99 = 2.3263478740408408   # norm.ppf(0.99)

var_95_1d = position * z_95 * sigma_1d
var_99_10d = position * z_99 * sigma_10d

result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}
# {'var_95_1d': 41790.24, 'var_99_10d': 186923.59}

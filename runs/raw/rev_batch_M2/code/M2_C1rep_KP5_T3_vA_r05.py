import math

P = 2_700_000
sigma_annual = 0.24
sigma_daily = sigma_annual / math.sqrt(252)
z_95 = 1.645
var_95_1d = round(P * sigma_daily * z_95, 2)

result = {
    'var_95_1d': var_95_1d
}

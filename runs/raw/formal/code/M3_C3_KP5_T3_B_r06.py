import math

vol_annual = 0.24
position = 2700000
z_95 = 1.6448536269514729  # norm.ppf(0.95)

vol_daily = vol_annual / math.sqrt(252)
var_95_1d = z_95 * vol_daily * position

result = {'var_95_1d': var_95_1d}

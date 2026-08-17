import math

position = 2_700_000
annual_vol = 0.24
daily_vol = annual_vol / math.sqrt(252)
z_95 = 1.645
var_95_1d = position * daily_vol * z_95

result = {
    'var_95_1d': round(var_95_1d, 2)
}

import math

annual_vol = 0.24
position = 2_700_000
z_score_95 = 1.645
trading_days = 252

daily_vol = annual_vol / math.sqrt(trading_days)
var_95_1d = position * daily_vol * z_score_95
result = {'var_95_1d': round(var_95_1d, 2)}

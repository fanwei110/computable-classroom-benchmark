import math
from scipy.stats import norm

position = 2700000
sigma_annual = 0.24
trading_days = 252

sigma_daily = sigma_annual / math.sqrt(trading_days)
z_95 = norm.ppf(0.95)
var_95_1d = position * z_95 * sigma_daily

result = {'var_95_1d': var_95_1d}

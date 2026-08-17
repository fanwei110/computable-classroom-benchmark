import scipy.stats as stats
import math

V = 1850000
sigma_ann = 0.218
T = 252

sigma_daily = sigma_ann / math.sqrt(T)

# 95% 1天 VaR
z_95 = stats.norm.ppf(0.95)
var_95_1d = V * z_95 * sigma_daily

# 99% 10天 VaR
z_99 = stats.norm.ppf(0.99)
sigma_10d = sigma_daily * math.sqrt(10)
var_99_10d = V * z_99 * sigma_10d

result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

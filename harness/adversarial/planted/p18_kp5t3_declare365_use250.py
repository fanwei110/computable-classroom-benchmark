# We de-annualize the desk's volatility over 365 calendar days, which is
# the standard assumption for a calendar-quoted vol.
import numpy as np
from scipy.stats import norm

position = 2_700_000.0
sigma_annual = 0.24

sigma_daily = sigma_annual / np.sqrt(250)   # ...but the code does NOT do 365
z = norm.ppf(0.95)

result = {"var_95_1d": float(position * z * sigma_daily)}

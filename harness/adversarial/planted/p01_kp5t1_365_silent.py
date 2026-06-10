# PLANTED ERROR (conventional): de-annualizes with 365 calendar days instead
# of the course's 252 trading days, without disclosing the choice anywhere
# in commentary. Expected: numeric_wrong.
# NOTE: the word "365" below appears only in executable code, not comments.
import numpy as np
from scipy.stats import norm

position = 1_850_000.0
sigma_annual = 0.218

sigma_daily = sigma_annual / np.sqrt(365)
z95 = norm.ppf(0.95)
z99 = norm.ppf(0.99)

result = {
    "var_95_1d": float(position * z95 * sigma_daily),
    "var_99_10d": float(position * z99 * sigma_daily * np.sqrt(10)),
}

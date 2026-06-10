# PLANTED ERROR (conventional, sign): reports VaR as a NEGATIVE number where
# the course convention is a positive loss amount. Expected: numeric_wrong.
import numpy as np
from scipy.stats import norm

position = 1_850_000.0
sigma_daily = 0.218 / np.sqrt(252)

result = {
    "var_95_1d": float(-position * norm.ppf(0.95) * sigma_daily),
    "var_99_10d": float(-position * norm.ppf(0.99) * sigma_daily * np.sqrt(10)),
}

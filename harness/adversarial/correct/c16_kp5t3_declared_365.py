# T3 solution using an ALTERNATIVE convention and SAYING SO.
# I assume the desk's 24% volatility is annualized over calendar days,
# so I de-annualize over 365 calendar days rather than trading days.
# Expected verdict: defensible (alternative convention, explicitly declared).
import numpy as np
from scipy.stats import norm

position = 2_700_000.0
sigma_annual = 0.24

days = 365
sigma_daily = sigma_annual / np.sqrt(days)

result = {
    "var_95_1d": float(position * norm.ppf(0.95) * sigma_daily),
    "convention_note": "de-annualized over 365 calendar days (declared assumption)",
}

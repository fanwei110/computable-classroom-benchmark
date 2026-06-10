# PLANTED ERROR (conceptual): uses the two-tailed critical values
# (1.96 / 2.576) for a one-tailed 95%/99% VaR. This is a misunderstanding of
# the VaR definition, not an alternative convention. Expected: numeric_wrong.
import numpy as np
from scipy.stats import norm

position = 1_850_000.0
sigma_daily = 0.218 / np.sqrt(252)

z95_twotailed = norm.ppf(0.975)
z99_twotailed = norm.ppf(0.995)

result = {
    "var_95_1d": float(position * z95_twotailed * sigma_daily),
    "var_99_10d": float(position * z99_twotailed * sigma_daily * np.sqrt(10)),
}

# Correct solution that emits warnings and writes to stderr
# (noise must not affect judging).
import sys
import warnings

import numpy as np
from scipy.stats import norm

warnings.warn("this is a deliberately noisy but correct solution")
print("starting VaR computation", file=sys.stderr)

position = 1_850_000.0
sigma_daily = 0.218 / np.sqrt(252)

warnings.warn("about to compute quantiles", category=UserWarning)

result = {
    "var_95_1d": float(position * norm.ppf(0.95) * sigma_daily),
    "var_99_10d": float(position * norm.ppf(0.99) * sigma_daily * np.sqrt(10)),
}
print("done", file=sys.stderr)

# Correct solution that stores `result` as a pandas Series (must be judged correct).
import numpy as np
import pandas as pd
from scipy.stats import norm

position = 1_850_000.0
sigma_daily = 0.218 / np.sqrt(252)

result = pd.Series({
    "var_95_1d": position * norm.ppf(0.95) * sigma_daily,
    "var_99_10d": position * norm.ppf(0.99) * sigma_daily * np.sqrt(10),
})

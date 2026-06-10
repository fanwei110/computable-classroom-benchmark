# Correct solution whose values are numpy scalars and 0-d arrays
# (must be judged correct after coercion).
import numpy as np
from scipy.stats import norm

s, k, sigma, r, t = 103.7, 97.5, 0.276, 0.043, 0.58

d1 = (np.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
d2 = d1 - sigma * np.sqrt(t)

result = {
    "call_price": np.float64(s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)),
    "call_delta": np.array(norm.cdf(d1)),                  # 0-d array
    "call_vega": np.float64(s * norm.pdf(d1) * np.sqrt(t)),
}

# PLANTED ERROR (conventional): quotes vega per PERCENTAGE POINT of
# volatility (dC/dsigma / 100) where the course quotes per unit.
# Expected: numeric_wrong (vega key fails).
import math

from scipy.stats import norm

s, k, sigma, r, t = 103.7, 97.5, 0.276, 0.043, 0.58

d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
d2 = d1 - sigma * math.sqrt(t)

result = {
    "call_price": s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2),
    "call_delta": norm.cdf(d1),
    "call_vega": s * norm.pdf(d1) * math.sqrt(t) / 100,
}

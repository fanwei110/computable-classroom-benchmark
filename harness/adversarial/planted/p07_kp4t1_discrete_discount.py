# PLANTED ERROR (conventional): discounts the strike with DISCRETE annual
# compounding (1+r)^-T where the course quotes option rates continuously
# compounded. Expected: numeric_wrong (price key fails).
import math

from scipy.stats import norm

s, k, sigma, r, t = 103.7, 97.5, 0.276, 0.043, 0.58

d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
d2 = d1 - sigma * math.sqrt(t)

df_discrete = (1 + r) ** (-t)

result = {
    "call_price": s * norm.cdf(d1) - k * df_discrete * norm.cdf(d2),
    "call_delta": norm.cdf(d1),
    "call_vega": s * norm.pdf(d1) * math.sqrt(t),
}

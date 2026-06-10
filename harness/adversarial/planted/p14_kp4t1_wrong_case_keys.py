# PLANTED ERROR (format): correct numbers stored under WRONG-CASE keys
# ("Call_Price" instead of "call_price"). The output contract is
# case-sensitive. Expected: format_failure (manual-review queue), never
# silently counted as a numerical error.
import math

from scipy.stats import norm

s, k, sigma, r, t = 103.7, 97.5, 0.276, 0.043, 0.58

d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
d2 = d1 - sigma * math.sqrt(t)

result = {
    "Call_Price": s * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2),
    "Call_Delta": norm.cdf(d1),
    "Call_Vega": s * norm.pdf(d1) * math.sqrt(t),
}

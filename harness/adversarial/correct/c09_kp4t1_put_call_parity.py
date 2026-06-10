# Correct solution computing the CALL via the put price and put-call parity
# (an equivalent route; must be judged correct).
import math

from scipy.stats import norm

s, k, sigma, r, t = 103.7, 97.5, 0.276, 0.043, 0.58

d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * math.sqrt(t))
d2 = d1 - sigma * math.sqrt(t)

put = k * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
call = put + s - k * math.exp(-r * t)          # parity

result = {
    "call_price": call,
    "call_delta": norm.cdf(d1),
    "call_vega": s * norm.pdf(d1) * math.sqrt(t),
}

import math
from scipy.stats import norm

S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58

d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

call_price = S * norm.cdf(d1) - K * math.exp(-r*T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * norm.pdf(d1) * math.sqrt(T)

result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

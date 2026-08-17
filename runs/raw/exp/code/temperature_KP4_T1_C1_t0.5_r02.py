import math
from scipy.stats import norm

S = 103.7
K = 97.5
r = 0.043
T = 0.58
sigma = 0.276

d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

call_price = S * norm.cdf(d1) - K * math.exp(-r*T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * math.sqrt(T) * norm.pdf(d1) * 0.01

result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

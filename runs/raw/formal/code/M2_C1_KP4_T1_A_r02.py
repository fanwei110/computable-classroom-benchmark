import math

S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58
q = 0.0

d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# Standard normal CDF approximation
def norm_cdf(x):
    # Abramowitz and Stegun formula 7.1.26
    a1 =  0.254829592
    a2 = -0.284496736
    a3 =  1.421413741
    a4 = -1.453152027
    a5 =  1.061405429
    p  =  0.3275911
    sign = 1 if x >= 0 else -1
    t = 1 / (1 + p * abs(x))
    y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x*x/2)
    return 0.5 * (1 + sign * y)

def norm_pdf(x):
    return math.exp(-x*x/2) / math.sqrt(2*math.pi)

Nd1 = norm_cdf(d1)
Nd2 = norm_cdf(d2)

call_price = S * math.exp(-q * T) * Nd1 - K * math.exp(-r * T) * Nd2
call_delta = math.exp(-q * T) * Nd1
call_vega = S * math.exp(-q * T) * norm_pdf(d1) * math.sqrt(T) * 0.01  # scaled to 1% change in volatility

result = {
    "call_price": round(call_price, 4),
    "call_delta": round(call_delta, 4),
    "call_vega": round(call_vega, 4)
}

result

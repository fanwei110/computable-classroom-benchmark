import math

S = 103.7
K = 97.5
iv = 0.276
r = 0.043
T = 0.58
delta_iv = 0.01

d1 = (math.log(S / K) + (r + 0.5 * iv**2) * T) / (iv * math.sqrt(T))
vega = S * math.exp(-0.5 * d1**2) / math.sqrt(2 * math.pi) * math.sqrt(T)

price_change = vega * delta_iv

result = {'price_change': round(price_change, 4)}

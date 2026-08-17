import math

S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58

d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
vega = S * math.exp(-d1**2 / 2) / math.sqrt(2 * math.pi) * math.sqrt(T)
price_change = vega * 0.01

result = {'price_change': price_change}

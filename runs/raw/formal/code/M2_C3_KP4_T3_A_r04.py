import math
import numpy as np

S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58

# d1 calculation
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
# vega: derivative of option price w.r.t volatility
vega = S * math.sqrt(T) * math.exp(-0.5 * d1**2) / math.sqrt(2 * math.pi)
# price change for a 1 percentage point increase in implied volatility (0.01 in decimal)
price_change = vega * 0.01

result = {'price_change': round(price_change, 4)}
print(result)

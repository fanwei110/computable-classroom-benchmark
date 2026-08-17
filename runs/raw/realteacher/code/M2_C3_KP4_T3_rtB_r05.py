import numpy as np
from scipy.stats import norm

S = 97.5
K = 103.7
sigma = 0.276
r = 0.043
T = 0.58

d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
vega = S * norm.pdf(d1) * np.sqrt(T)
price_change = vega * 0.01

result = {'price_change': round(price_change, 6)}
print(result)

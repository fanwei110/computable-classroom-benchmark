import numpy as np
from scipy.stats import norm

# 参数
S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58
q = 0.0  # 未说明红利，按无连续红利处理

vol_bump = 0.01  # 隐含波动率上升 1 个百分点：0.276 -> 0.286

# Black-Scholes 闭式解
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 价格、delta、vega
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
delta = np.exp(-q * T) * norm.cdf(d1)
vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)  # dPrice/dsigma，单位波动率

# 价格对 +1% 波动率的一阶响应
price_change = vega * vol_bump

result = {'price_change': float(price_change)}

print(f"call_price = {call_price:.6f}")
print(f"delta = {delta:.6f}")
print(f"vega = {vega:.6f}")
print(f"price_change = {price_change:.6f}")
print(result)

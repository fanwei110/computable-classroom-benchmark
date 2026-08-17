import numpy as np
from scipy.stats import norm

# 参数
S = 103.7          # 标的价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率 27.6%
r = 0.043          # 连续复利利率 4.3%
tau = 0.58         # 剩余期限，年
vol_shift = 0.01   # 波动率上涨 1 个百分点

# 假设：欧式期权、无红利。vega 对欧式看涨/看跌相同。

def bs_d1(S, K, sigma, r, tau):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * tau) / (sigma * np.sqrt(tau))

def bs_d2(S, K, sigma, r, tau):
    return bs_d1(S, K, sigma, r, tau) - sigma * np.sqrt(tau)

def bs_vega(S, K, sigma, r, tau):
    d1 = bs_d1(S, K, sigma, r, tau)
    return S * norm.pdf(d1) * np.sqrt(tau)

# 数学 vega = dPrice/dsigma，sigma 以小数表示；
# 因此 1 个百分点波动率变化对应 vega * 0.01
vega = bs_vega(S, K, sigma, r, tau)
price_change = vega * vol_shift

result = {'price_change': float(price_change)}
print(result)

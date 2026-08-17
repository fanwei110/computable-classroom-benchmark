import numpy as np
from scipy.stats import norm

def bs_call(S, K, T, r, sigma):
    """Black-Scholes 欧式看涨期权定价"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 给定参数
S = 103.7          # 标的价格
K = 97.5           # 行权价
T = 0.58           # 剩余期限（年）
r = 0.043          # 无风险利率
sigma0 = 0.276     # 初始隐含波动率（27.6%）
dsigma = 0.01      # 波动率上升一个百分点（0.01）

# 计算期权价格变化（精确值）
C0 = bs_call(S, K, T, r, sigma0)
C1 = bs_call(S, K, T, r, sigma0 + dsigma)
price_change = C1 - C0

result = {'price_change': price_change}
print(result)

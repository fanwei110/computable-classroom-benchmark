import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    欧式看涨期权 Black-Scholes 定价（连续复利）
    S: 标的现价
    K: 行权价
    T: 剩余期限（年）
    r: 无风险利率（连续复利，小数）
    sigma: 波动率（小数）
    返回: 看涨期权价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 给定参数
S = 103.7      # 标的现价
K = 97.5       # 行权价
T = 0.58       # 剩余年限
r = 0.043      # 无风险利率（连续复利）
sigma1 = 0.276 # 当前隐含波动率 27.6%
sigma2 = 0.286 # 上升一个百分点后的波动率 28.6%

# 重定价
call_price_1 = black_scholes_call(S, K, T, r, sigma1)
call_price_2 = black_scholes_call(S, K, T, r, sigma2)

# 精确价差：波动率上升一个百分点时期权价格的涨幅
price_change = call_price_2 - call_price_1

# 输出结果
result = {'price_change': price_change}
print(result)

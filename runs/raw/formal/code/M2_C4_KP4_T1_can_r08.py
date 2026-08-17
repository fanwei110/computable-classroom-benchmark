import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权的价格、Delta 和 Vega（每单位波动率）。
    参数：
        S: 标的现价
        K: 行权价
        T: 剩余期限（年）
        r: 无风险利率（连续复利，小数）
        sigma: 波动率（小数）
    返回：
        price: 期权价格
        delta: N(d1)
        vega: dC/dσ （对波动率σ的偏导数，小数形式）
    """
    # 1. 计算 d1 和 d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 2. 价格与 Delta
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    delta = norm.cdf(d1)
    
    # 3. Vega: dC/dσ = S * sqrt(T) * N'(d1)   （N' 为标准正态密度函数）
    vega = S * np.sqrt(T) * norm.pdf(d1)
    
    return price, delta, vega

# 给定参数
S = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276

call_price, call_delta, call_vega = black_scholes_call(S, K, T, r, sigma)

# 输出结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

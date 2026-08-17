import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    欧式看涨期权定价（无分红）
    S: 标的现价
    K: 行权价
    T: 剩余到期时间（年）
    r: 无风险利率（连续复利）
    sigma: 隐含波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # 价格
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    # Delta
    call_delta = norm.cdf(d1)
    
    # Vega（对波动率1%变动的敏感度，即 dC/d(sigma)）
    # 注意：Vega = S * sqrt(T) * norm.pdf(d1) / 100  如果以1%为单位
    # 这里给出的是原始Vega（即波动率变动1单位（100%）的敏感度），通常用除以100表示1%变动
    # 按照惯例，给出除以100的值，表示波动率变动1个百分点（如27.6%到28.6%）的价格变动
    call_vega = S * np.sqrt(T) * norm.pdf(d1) / 100.0
    
    return call_price, call_delta, call_vega

# 参数
S = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276  # 27.6%

price, delta, vega = black_scholes_call(S, K, T, r, sigma)

result = {
    'call_price': round(price, 6),
    'call_delta': round(delta, 6),
    'call_vega': round(vega, 6)
}

print(result)

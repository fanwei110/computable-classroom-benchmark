import numpy as np
from scipy.stats import norm

def black_scholes_vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * norm.pdf(d1)
    return vega

# 示例参数
S = 100
K = 100
T = 0.5  # 半年
r = 0.05
sigma = 0.2

vega = black_scholes_vega(S, K, T, r, sigma)
price_change = vega * 0.01  # 隐波变化1个点（0.01）

result = {
    'price_change': price_change
}

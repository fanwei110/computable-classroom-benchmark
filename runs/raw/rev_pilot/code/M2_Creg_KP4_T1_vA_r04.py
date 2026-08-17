import numpy as np
from scipy.stats import norm
import pandas as pd          # 按要求导入，未使用
import matplotlib.pyplot as plt  # 按要求导入，未使用

def black_scholes_call(S, K, T, r, sigma):
    """
    计算不分红股票欧式看涨期权的价格、Delta 和 Vega。
    Vega 是价格对波动率（小数形式）的偏导数。
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    call_delta = norm.cdf(d1)
    call_vega = S * norm.pdf(d1) * np.sqrt(T)   # 价格对 σ 的偏导数 (σ 为小数)
    
    return call_price, call_delta, call_vega

# 给定参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 年化波动率 (27.6%)
r = 0.043          # 年化无风险利率 (4.3%)
T = 0.58           # 剩余期限 (年)

price, delta, vega = black_scholes_call(S, K, T, r, sigma)

result = {
    'call_price': price,
    'call_delta': delta,
    'call_vega': vega
}

if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.6f}")

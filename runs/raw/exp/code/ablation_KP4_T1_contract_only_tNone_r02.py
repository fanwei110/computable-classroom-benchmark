import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# 输入参数
S = 103.7      # 标的价格
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率（27.6%）
r = 0.043      # 无风险利率（4.3%）
T = 0.58       # 剩余期限（年）

# Black-Scholes 计算
def black_scholes_call_price(S, K, T, r, sigma):
    """
    计算欧式看涨期权价格
    """
    if T <= 0:
        return max(0, S - K)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权 Delta
    """
    if T <= 0:
        return 1.0 if S >= K else 0.0
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

def black_scholes_vega(S, K, T, r, sigma):
    """
    计算欧式看涨期权 Vega
    """
    if T <= 0:
        return 0.0
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    return vega

# 计算期权价格、delta 和 vega
call_price = black_scholes_call_price(S, K, T, r, sigma)
call_delta = black_scholes_delta(S, K, T, r, sigma)
call_vega = black_scholes_vega(S, K, T, r, sigma)

# 输出结果
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print("计算结果：")
print(f"看涨期权价格: {result['call_price']}")
print(f"Delta: {result['call_delta']}")
print(f"Vega: {result['call_vega']}")

# 双重检查：用更精确的数值
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

print("\n详细参数验证：")
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print(f"N(d1) = {norm.cdf(d1):.6f}")
print(f"N(d2) = {norm.cdf(d2):.6f}")
print(f"n(d1) = {norm.pdf(d1):.6f}")

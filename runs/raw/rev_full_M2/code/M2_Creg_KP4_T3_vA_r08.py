import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """计算欧式看涨期权价格"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 参数设置
S = 103.7          # 现价
K = 97.5           # 行权价
sigma = 0.276      # 当前波动率
r = 0.043          # 无风险利率
T = 0.58           # 剩余时间（年）
delta_sigma = 0.01 # 波动率变化（一个百分点）

# 计算当前期权价格
price_current = black_scholes_call(S, K, T, r, sigma)

# 计算波动率上升后的期权价格
price_up = black_scholes_call(S, K, T, r, sigma + delta_sigma)

# 价格变化
price_change = price_up - price_current

# 存入结果字典
result = {
    'price_change': price_change
}

# 输出结果
print(f"当前波动率: {sigma:.4f}")
print(f"新波动率: {sigma + delta_sigma:.4f}")
print(f"当前期权价格: {price_current:.6f}")
print(f"新期权价格: {price_up:.6f}")
print(f"价格变化: {price_change:.6f}")
print(f"\n结果字典: {result}")

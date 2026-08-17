import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """欧式看涨期权的 Black-Scholes 定价（连续复利）"""
    if T <= 0:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 输入参数
S = 103.7        # 现价
K = 97.5         # 行权价
T = 0.58         # 剩余年限
r = 0.043        # 无风险利率（连续复利）
sigma1 = 0.276   # 波动率 27.6%
sigma2 = 0.286   # 波动率 28.6%

# 定价
price1 = black_scholes_call(S, K, T, r, sigma1)
price2 = black_scholes_call(S, K, T, r, sigma2)

# 价差
price_change = price2 - price1

# 结果字典
result = {
    'price_change': price_change
}

# 打印输出（保留6位小数）
print("Black-Scholes 欧式看涨期权定价")
print(f"标的现价: {S}, 行权价: {K}, 剩余期限: {T} 年, 利率: {r}")
print(f"波动率 27.6% 下的期权价格: {price1:.6f}")
print(f"波动率 28.6% 下的期权价格: {price2:.6f}")
print(f"波动率上升一个百分点带来的价格变动: {price_change:.6f}")
print(f"\n结果字典: {result}")

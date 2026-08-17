import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """计算欧式看涨期权的 Black-Scholes 价格"""
    if T <= 0:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 给定参数
S = 103.7       # 标的现价
K = 97.5        # 行权价
T = 0.58        # 剩余时间（年）
r = 0.043       # 无风险利率
sigma0 = 0.276  # 当前隐含波动率
delta_sigma = 0.01  # 波动率上升一个百分点（即1%）

# 计算当前波动率下的期权价格
price_old = black_scholes_call(S, K, T, r, sigma0)
# 计算波动率上升后的期权价格
price_new = black_scholes_call(S, K, T, r, sigma0 + delta_sigma)

# 价格变化
price_change = price_new - price_old

# 将结果存入字典
result = {
    'price_change': price_change
}

# 输出结果（方便投屏查看）
print(f"当前波动率 {sigma0*100:.1f}% 下的期权价格: {price_old:.4f}")
print(f"波动率上升至 {(sigma0+delta_sigma)*100:.1f}% 时的期权价格: {price_new:.4f}")
print(f"期权价格变化 (price_change): {price_change:.6f}")
print("\n结果字典:")
print(result)

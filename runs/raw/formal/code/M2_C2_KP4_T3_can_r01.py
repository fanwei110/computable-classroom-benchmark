import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格。
    
    参数：
    S : 标的资产现价
    K : 行权价
    T : 剩余到期时间（年）
    r : 无风险利率（连续复利，小数）
    sigma : 波动率（小数）
    
    返回：
    看涨期权价格
    """
    if T <= 0:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 给定参数
S0 = 103.7
K = 97.5
sigma_base = 0.276   # 27.6%
r = 0.043            # 4.3%
T = 0.58             # 0.58 年
delta_sigma = 0.01   # 上升一个百分点

# 计算初始波动率下的期权价格
price_base = black_scholes_call(S0, K, T, r, sigma_base)

# 计算波动率上升一个百分点后的期权价格
sigma_new = sigma_base + delta_sigma
price_new = black_scholes_call(S0, K, T, r, sigma_new)

# 价格变化
price_change = price_new - price_base

# 按要求存入字典
result = {
    'price_change': price_change
}

# 打印结果以便课堂投屏展示
print(f"初始波动率 {sigma_base*100:.1f}% 下的期权价格: {price_base:.6f}")
print(f"波动率上升至 {sigma_new*100:.1f}% 后的期权价格: {price_new:.6f}")
print(f"期权价格变化 (price_change): {price_change:.6f}")
print("\n结果字典:")
print(result)

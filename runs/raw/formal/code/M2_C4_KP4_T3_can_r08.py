import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    Black-Scholes 欧式看涨期权定价公式（连续复利）
    
    参数:
    S: 标的资产现价
    K: 行权价
    T: 剩余期限（年）
    r: 无风险利率（连续复利，小数形式）
    sigma: 波动率（小数形式）
    
    返回:
    期权价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 给定参数
S = 103.7        # 标的资产现价
K = 97.5         # 行权价
T = 0.58         # 剩余期限（年）
r = 0.043        # 无风险利率（4.3%）
sigma_original = 0.276   # 原始波动率（27.6%）
sigma_new = 0.286        # 新波动率（28.6%）

# 步骤1：在两个波动率下精确重定价
price_original = black_scholes_call(S, K, T, r, sigma_original)
price_new = black_scholes_call(S, K, T, r, sigma_new)

# 计算精确价差
price_change = price_new - price_original

# 输出结果存入字典
result = {
    'price_change': price_change
}

# 打印结果以便验证
print(f"原始波动率 (27.6%) 下的期权价格: {price_original:.6f}")
print(f"新波动率 (28.6%) 下的期权价格: {price_new:.6f}")
print(f"波动率上升1个百分点导致的价格变化: {price_change:.6f}")
print(f"\n结果字典: {result}")

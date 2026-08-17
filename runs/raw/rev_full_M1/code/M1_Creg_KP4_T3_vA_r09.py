import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算 Black-Scholes 看涨期权价格
    S: 标的资产现价
    K: 行权价
    T: 剩余期限（年）
    r: 无风险利率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 输入参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
T = 0.58       # 剩余期限（年）
r = 0.043      # 无风险利率
sigma_initial = 0.276  # 初始波动率
sigma_increased = sigma_initial + 0.01  # 波动率上升1个百分点

# 计算初始期权价格
price_initial = black_scholes_call(S, K, T, r, sigma_initial)

# 计算波动率上升后的期权价格
price_increased = black_scholes_call(S, K, T, r, sigma_increased)

# 计算价格变化
price_change = price_increased - price_initial

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，便于调试）
print(result)

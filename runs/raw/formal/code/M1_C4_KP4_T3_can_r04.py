import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7      # 现价
K = 97.5       # 行权价
sigma_original = 0.276  # 原始波动率
sigma_new = 0.286       # 新波动率（上升1个百分点）
r = 0.043      # 无风险利率（连续复利）
T = 0.58       # 剩余期限（年）

# Black-Scholes 欧式看涨期权定价函数
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 计算原始波动率下的期权价格
price_original = black_scholes_call(S, K, T, r, sigma_original)

# 计算新波动率下的期权价格
price_new = black_scholes_call(S, K, T, r, sigma_new)

# 计算价格变化
price_change = price_new - price_original

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，用于验证）
print(result)

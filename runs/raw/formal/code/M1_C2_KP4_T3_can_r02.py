import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
sigma = 0.276      # 波动率 (27.6%)
r = 0.043          # 无风险利率 (4.3%)
T = 0.58           # 剩余期限 (年)
d_sigma = 0.01     # 波动率变化 (1%)

# Black-Scholes 欧式看涨期权定价函数
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 计算初始期权价格
initial_price = black_scholes_call(S, K, T, r, sigma)

# 计算波动率上升1%后的期权价格
new_sigma = sigma + d_sigma
new_price = black_scholes_call(S, K, T, r, new_sigma)

# 计算价格变化
price_change = new_price - initial_price

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，用于验证）
print(result)

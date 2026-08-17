import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余期限 (年)

# Black-Scholes 欧式看涨期权定价函数
def black_scholes_call(S, K, sigma, r, T):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 计算 Vega (期权价格对波动率的敏感度)
def vega(S, K, sigma, r, T):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega_value = S * norm.pdf(d1) * np.sqrt(T)
    return vega_value

# 当前期权价格
current_price = black_scholes_call(S, K, sigma, r, T)

# 计算 Vega (每 1% 波动率变化对应的价格变化)
vega_value = vega(S, K, sigma, r, T) / 100  # 转换为 1% 变化

# 波动率上升 1% 后的期权价格变化
sigma_new = sigma + 0.01
new_price = black_scholes_call(S, K, sigma_new, r, T)
price_change = new_price - current_price

# 使用 Vega 近似验证
price_change_approx = vega_value * 1  # 1% 变化

# 存储结果
result = {
    'price_change': price_change  # 精确计算的价格变化
}

# 输出结果（可选，便于调试）
print("期权价格变化 (精确计算):", result['price_change'])
print("期权价格变化 (Vega 近似):", price_change_approx)

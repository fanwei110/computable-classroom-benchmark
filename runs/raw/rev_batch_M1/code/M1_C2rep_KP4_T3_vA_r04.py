import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
sigma = 0.276      # 波动率 (27.6%)
r = 0.043          # 无风险利率 (4.3%)
T = 0.58           # 剩余期限 (年)

# Black-Scholes 欧式看涨期权定价函数
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 计算 vega (期权价格对波动率的敏感度)
def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega_value = S * norm.pdf(d1) * np.sqrt(T)
    return vega_value

# 计算初始期权价格
initial_price = black_scholes_call(S, K, T, r, sigma)

# 计算初始 vega
initial_vega = vega(S, K, T, r, sigma)

# 波动率上升 1 个百分点 (0.01)
sigma_increased = sigma + 0.01

# 计算新的期权价格
new_price = black_scholes_call(S, K, T, r, sigma_increased)

# 通过 vega 近似计算价格变化 (vega * Δsigma)
price_change_approx = initial_vega * 0.01

# 精确计算价格变化 (新价格 - 初始价格)
price_change_exact = new_price - initial_price

# 结果存储 (使用精确计算的价格变化)
result = {
    'price_change': price_change_exact
}

# 输出结果 (可选，便于调试)
print("Initial option price:", initial_price)
print("New option price after volatility increase:", new_price)
print("Price change (exact):", price_change_exact)
print("Price change (vega approximation):", price_change_approx)
print("Result dictionary:", result)

import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（27.6%）
r = 0.043          # 无风险利率（4.3%）
T = 0.58           # 到期时间（0.58年）

# Black-Scholes模型的辅助函数
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

# 计算初始期权价格（假设为看涨期权）
option_price_initial = black_scholes(S, K, T, r, sigma, 'call')

# 计算vega（每1%波动率变化对应的价格变化）
vega_value = vega(S, K, T, r, sigma) / 100  # 因为vega通常表示为每1%变化的价格变化

# 波动率增加1个百分点（即0.01）时的价格变化
sigma_new = sigma + 0.01
option_price_new = black_scholes(S, K, T, r, sigma_new, 'call')
price_change = option_price_new - option_price_initial

# 使用vega近似验证
price_change_approx = vega_value * 1  # 1个百分点变化

# 存储结果
result = {
    'price_change': price_change  # 精确计算的价格变化
}

# 输出结果（可选，用于调试）
print("Initial Option Price:", option_price_initial)
print("New Option Price (IV +1%):", option_price_new)
print("Price Change (Exact):", price_change)
print("Price Change (Vega Approx):", price_change_approx)

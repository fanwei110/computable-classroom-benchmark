import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产价格
K = 97.5           # 行权价
sigma = 0.276      # 波动率 (27.6%)
r = 0.043          # 无风险利率 (4.3%)
T = 0.58           # 剩余期限 (年)

# 计算 Black-Scholes 期权价格和希腊字母
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = -norm.cdf(-d1)

    vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # 每 1% 波动率变化的 Vega
    return price, delta, vega

# 计算初始期权价格和 Vega
initial_price, delta, vega = black_scholes(S, K, T, r, sigma)

# 波动率变化 1 个百分点 (0.01) 时的价格变化
sigma_change = 0.01
price_change = vega * sigma_change / 0.01  # 等价于 vega * 1 (因为 vega 已经是每 1% 的变化)

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，便于调试）
print("期权价格变化:", result['price_change'])

import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（27.6%）
r = 0.043          # 无风险利率（4.3%）
T = 0.58           # 到期时间（0.58年）

# Black-Scholes模型计算欧式期权价格和Vega
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # Vega通常表示为波动率变化1%时的价格变化
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # 看跌期权Vega与看涨期权相同

    return price, vega

# 计算初始价格和Vega
initial_price, vega = black_scholes(S, K, T, r, sigma)

# 波动率增加1个百分点（0.01）
sigma_new = sigma + 0.01
new_price, _ = black_scholes(S, K, T, r, sigma_new)

# 价格变化
price_change = new_price - initial_price

# 存入结果
result = {
    'price_change': price_change
}

# 输出结果（可选，便于调试）
print("Price change when IV increases by 1%:", result['price_change'])

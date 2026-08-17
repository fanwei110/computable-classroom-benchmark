import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7      # 现价
K = 97.5       # 行权价
sigma1 = 0.276 # 原始波动率
sigma2 = 0.286 # 波动率上升1个百分点后
r = 0.043      # 无风险利率（连续复利）
T = 0.58       # 剩余期限（年）

# Black-Scholes 欧式看涨期权定价函数
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 计算两种波动率下的期权价格
price_sigma1 = black_scholes_call(S, K, T, r, sigma1)
price_sigma2 = black_scholes_call(S, K, T, r, sigma2)

# 计算价格变化
price_change = price_sigma2 - price_sigma1

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，用于验证）
print(result)

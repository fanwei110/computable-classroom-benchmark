import numpy as np
from scipy.stats import norm

def bs_call_price(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 期权参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
T = 0.58           # 剩余期限（年）
r = 0.043          # 无风险利率
sigma_initial = 0.276  # 初始隐含波动率
sigma_new = 0.286     # 上升一个百分点后的隐含波动率

# 计算初始波动率下的期权价格
price_initial = bs_call_price(S, K, T, r, sigma_initial)

# 计算新波动率下的期权价格
price_new = bs_call_price(S, K, T, r, sigma_new)

# 计算期权价格的变化量
price_change = price_new - price_initial

# 按照 output contract 将结果存入字典
result = {
    'price_change': price_change
}

print(result)

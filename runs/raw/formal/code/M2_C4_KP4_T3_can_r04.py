import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格（连续复利）
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 市场参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
T = 0.58           # 剩余时间（年）
r = 0.043          # 无风险利率（连续复利）
sigma_base = 0.276 # 当前隐含波动率 27.6%
sigma_new  = 0.286 # 上升一个百分点后的波动率 28.6%

# 精确重定价
price_base = black_scholes_call(S, K, T, r, sigma_base)
price_new  = black_scholes_call(S, K, T, r, sigma_new)

# 计算精确价差
price_change = price_new - price_base

# 按要求存入字典
result = {'price_change': price_change}

if __name__ == "__main__":
    print(f"波动率 {sigma_base:.1%} 下的期权价格: {price_base:.6f}")
    print(f"波动率 {sigma_new:.1%} 下的期权价格: {price_new:.6f}")
    print(f"精确价差 (price_change): {price_change:.6f}")
    print(f"result = {result}")

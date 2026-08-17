import numpy as np
from scipy.stats import norm

# ------------------------------
# 1. 定义给定参数
# ------------------------------
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 当前隐含波动率
r = 0.043          # 无风险利率
T = 0.58           # 剩余年限
delta_sigma = 0.01 # 波动率上升一个百分点 (100 bps)

# ------------------------------
# 2. Black-Scholes 看涨期权定价函数
# ------------------------------
def bs_call_price(S, K, T, r, sigma):
    """返回欧式看涨期权的 Black-Scholes 价格"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# ------------------------------
# 3. 计算价格变化（精确重定价法）
# ------------------------------
price_base = bs_call_price(S, K, T, r, sigma)
price_up   = bs_call_price(S, K, T, r, sigma + delta_sigma)
price_change = price_up - price_base

# ------------------------------
# 4. 按要求存入 result 字典
# ------------------------------
result = {'price_change': price_change}

# 教师投屏时可直观查看输出
if __name__ == '__main__':
    print(result)

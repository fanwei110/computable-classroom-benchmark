import numpy as np
from scipy.stats import norm

# 欧式看涨期权的 Black-Scholes 定价公式
def bs_call_price(S, K, T, r, sigma):
    """计算欧式看涨期权的价格"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 给定参数
S = 103.7        # 标的资产价格
K = 97.5         # 行权价
T = 0.58         # 剩余期限（年）
r = 0.043        # 无风险利率
sigma_base = 0.276   # 原始隐含波动率
sigma_up = 0.286     # 上涨一个百分点后的隐含波动率

# 计算两种波动率下的期权价格
price_base = bs_call_price(S, K, T, r, sigma_base)
price_up = bs_call_price(S, K, T, r, sigma_up)

# 价格变化 = 新价格 - 原价格
price_change = price_up - price_base

# 按要求存入字典
result = {'price_change': price_change}

# 输出结果（课堂投屏可见）
print(result)

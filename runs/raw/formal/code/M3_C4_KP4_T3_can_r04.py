import numpy as np
from scipy.stats import norm

# ================= 基础参数设定 =================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
T = 0.58        # 剩余期限（年）
r = 0.043       # 无风险利率（连续复利）
sigma_1 = 0.276 # 初始波动率
sigma_2 = 0.286 # 隐含波动率上升一个百分点后的波动率

# ================= Black-Scholes 定价函数 =================
def bs_call_price(S, K, T, r, sigma):
    """
    欧式看涨期权的 Black-Scholes 定价公式
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# ================= 计算与结果 =================
# 1. 分别在波动率 28.6% 与 27.6% 下精确重定价
price_sigma_2 = bs_call_price(S, K, T, r, sigma_2)
price_sigma_1 = bs_call_price(S, K, T, r, sigma_1)

# 2. 把精确价差存入 result
price_change = price_sigma_2 - price_sigma_1

result = {
    'price_change': price_change
}

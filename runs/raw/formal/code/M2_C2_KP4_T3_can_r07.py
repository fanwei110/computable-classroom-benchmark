import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格。

    参数:
        S : 标的资产现价
        K : 行权价
        T : 剩余期限（年）
        r : 无风险利率（连续复利）
        sigma : 波动率（年化）
    返回:
        期权价格
    """
    if sigma <= 0 or T <= 0:
        # 处理边界情况，避免除零
        return max(S - K * np.exp(-r * T), 0.0)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price


# 给定参数
S = 103.7        # 现价
K = 97.5         # 行权价
T = 0.58         # 剩余年限
r = 0.043        # 无风险利率
sigma_old = 0.276  # 当前隐含波动率

# 波动率上升一个百分点（0.01）
sigma_new = sigma_old + 0.01

# 计算变动前后的期权价格
price_old = black_scholes_call(S, K, T, r, sigma_old)
price_new = black_scholes_call(S, K, T, r, sigma_new)

# 价格变化
price_change = price_new - price_old

# 按要求存入 result 字典
result = {'price_change': price_change}

# 输出结果，方便教师查看
print(result)

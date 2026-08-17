import numpy as np
from scipy.stats import norm

# 市场参数与期权信息
S = 103.7      # 标的现价
K = 97.5       # 行权价
T = 0.58       # 剩余期限（年）
r = 0.043      # 无风险利率（连续复利）
sigma_1 = 0.276 # 初始波动率 27.6%
sigma_2 = 0.286 # 上升一个百分点后的波动率 28.6%

# 欧式看涨期权 Black-Scholes 定价公式
def bs_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 步骤1：分别在 27.6% 与 28.6% 的波动率下精确重定价
price_sigma_1 = bs_call_price(S, K, T, r, sigma_1)
price_sigma_2 = bs_call_price(S, K, T, r, sigma_2)

# 步骤2：计算精确价差
price_change = price_sigma_2 - price_sigma_1

# 按契约输出结果
result = {
    'price_change': price_change
}

# 课堂投屏辅助打印（可选，便于直观展示）
print(f"波动率 27.6% 下的期权价格: {price_sigma_1:.4f}")
print(f"波动率 28.6% 下的期权价格: {price_sigma_2:.4f}")
print(f"期权价格变化: {price_change:.4f}")
print(f"result字典: {result}")

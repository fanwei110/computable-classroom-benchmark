import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    欧式看涨期权的 Black-Scholes 定价公式（连续复利，无股息）
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 参数设定（小数表示）
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
T = 0.58       # 剩余期限（年）
r = 0.043      # 无风险利率（连续复利）
sigma_low = 0.276   # 原波动率 27.6%
sigma_high = 0.286  # 上升一个百分点后的波动率 28.6%

# 1. 分别在两个波动率下精确重定价
price_at_27_6 = black_scholes_call(S, K, T, r, sigma_low)
price_at_28_6 = black_scholes_call(S, K, T, r, sigma_high)

# 2. 计算精确价差
price_change = price_at_28_6 - price_at_27_6

# 按照输出契约存入字典
result = {
    'price_change': price_change
}

# 课堂投屏展示结果
print(f"波动率 27.6% 下的看涨期权价格: {price_at_27_6:.4f}")
print(f"波动率 28.6% 下的看涨期权价格: {price_at_28_6:.4f}")
print(f"隐含波动率上升1%带来的期权价格变化: {price_change:.4f}")
print(f"\nresult = {result}")

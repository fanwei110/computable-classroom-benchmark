import numpy as np
from scipy.stats import norm

# ==================== 参数设置 ====================
S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 波动率 (27.6%)
r = 0.043        # 无风险利率 (4.3%)
T = 0.58         # 剩余期限 (年)
delta_sigma = 0.01  # 波动率上升一个百分点 (1%)

# ==================== Black-Scholes 闭式解 ====================
def bs_call_price(S, K, T, r, sigma):
    """计算欧式看涨期权价格"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# ==================== 推算价格变化 ====================
# 计算原波动率下的期权价格
price_original = bs_call_price(S, K, T, r, sigma)

# 计算波动率上升1个百分点后的期权价格
price_new = bs_call_price(S, K, T, r, sigma + delta_sigma)

# 价格的变化量
price_change = price_new - price_original

# (附注：也可通过希腊字母 Vega 线性近似：Vega = S * sqrt(T) * norm.pdf(d1)，price_change ≈ Vega * delta_sigma)
# 此处直接使用精确价格差值，避免了泰勒展开的截断误差，最为严谨。

# ==================== 输出契约 ====================
result = {
    'price_change': price_change
}

print(result)

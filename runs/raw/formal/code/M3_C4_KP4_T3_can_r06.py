import numpy as np
from scipy.stats import norm

# ================= 市场参数 =================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
r = 0.043       # 无风险利率 (连续复利)
T = 0.58        # 剩余期限 (年)
sigma_1 = 0.276 # 初始波动率 (27.6%)
sigma_2 = 0.286 # 上升1个百分点后的波动率 (28.6%)

# ================= BS模型欧式看涨期权定价公式 =================
def bs_call_price(S, K, r, T, sigma):
    """
    计算无股息欧式看涨期权的Black-Scholes价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# ================= 步骤1：分别在两个波动率下精确重定价 =================
price_sigma_1 = bs_call_price(S, K, r, T, sigma_1)
price_sigma_2 = bs_call_price(S, K, r, T, sigma_2)

# ================= 步骤2：计算精确价差并存入result =================
price_change = price_sigma_2 - price_sigma_1

# 按照输出契约存入字典
result = {
    'price_change': price_change
}

# ================= 课堂投屏展示 =================
print(f"【参数设定】现价: {S}, 行权价: {K}, 利率: {r}, 期限: {T}")
print(f"波动率 {sigma_1*100:.1f}% 时的看涨期权精确价格: {price_sigma_1:.4f}")
print(f"波动率 {sigma_2*100:.1f}% 时的看涨期权精确价格: {price_sigma_2:.4f}")
print(f"隐含波动率上升1%引起的期权价格变化: {price_change:.4f}")
print("-" * 50)
print("输出契约 result:", result)

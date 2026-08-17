import numpy as np
from scipy.stats import norm

# ==========================================
# 欧式看涨期权 Black-Scholes 定价与希腊字母
# ==========================================

# 1. 基础参数设定
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 当前波动率 (27.6%)
r = 0.043       # 无风险连续复利利率 (4.3%)
T = 0.58        # 剩余期限 (年)
# 假设：无分红

# 2. 定义BS看涨期权定价辅助函数
def bs_call_price(S, K, r, T, sigma):
    """计算欧式看涨期权价格与 d1"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price, d1

# 3. 计算当前状态下的期权价格与希腊字母 Vega
price_initial, d1_initial = bs_call_price(S, K, r, T, sigma)

# Vega 闭式解: Vega = dC/d(sigma) = S * sqrt(T) * N'(d1)
# 表示波动率变化 1 个单位 (即100%) 时期权价格的绝对变化量
vega = S * np.sqrt(T) * norm.pdf(d1_initial)

# 4. 推算波动率上升 1 个百分点 (即 0.01) 的价格响应
# 方法一：基于希腊字母 Vega 的一阶线性推算 (课堂讲授希腊字母意义的标准做法)
price_change_by_vega = vega * 0.01

# 方法二：基于定价公式的精确差值 (验证线性近似的准确性)
sigma_new = sigma + 0.01  # 波动率上升1个百分点，变为28.6%
price_new, _ = bs_call_price(S, K, r, T, sigma_new)
price_change_exact = price_new - price_initial

# 由于 1% 的变化极小，Vega 的线性推算与精确差值高度一致。
# 将精确差值存入字典，客观回答“如果上升一个百分点，涨多少”
result = {'price_change': price_change_exact}

# ------------------------------------------
# 课堂投屏辅助打印 (便于教师展示与讲解)
# ------------------------------------------
print(f"=== Black-Scholes 期权定价与 Vega 推算 ===")
print(f"当前波动率下的看涨期权价格: {price_initial:.4f}")
print(f"Vega (闭式解)            : {vega:.4f}")
print(f"-" * 45)
print(f"波动率上升 1% (0.01) 后:")
print(f"  基于 Vega 的线性推算响应 : {price_change_by_vega:.4f}")
print(f"  基于公式重算的精确响应   : {price_change_exact:.4f}")
print(f"-" * 45)
print(f"最终存入字典的结果: {result}")

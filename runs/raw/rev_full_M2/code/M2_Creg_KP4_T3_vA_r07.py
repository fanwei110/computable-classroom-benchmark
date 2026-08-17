
import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# ============================
# 定义看涨期权定价函数
# ============================
def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """利用 Black-Scholes 公式计算欧式看涨期权的理论价格"""
    if T <= 0.0:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# ============================
# 输入参数
# ============================
S        = 103.7      # 标的资产现价
K        = 97.5       # 行权价
sigma    = 0.276      # 当前隐含波动率 (27.6%)
r        = 0.043      # 无风险利率 (4.3%)
T        = 0.58       # 剩余期限（年）

# ============================
# 计算价格变化
# ============================
price_current = black_scholes_call(S, K, T, r, sigma)

sigma_new = sigma + 0.01   # 波动率上升一个百分点 -> 28.6%
price_new  = black_scholes_call(S, K, T, r, sigma_new)

price_change = price_new - price_current

# ============================
# 按照输出契约存放结果
# ============================
result = {'price_change': price_change}

print(result)

# 可选：给出更直观的输出
print(f"当前波动率 ({sigma:.1%}) 下的期权价格：{price_current:.4f}")
print(f"波动率上升 1 个百分点 ({sigma_new:.1%}) 后的期权价格：{price_new:.4f}")
print(f"价格变动：{price_change:.4f}")

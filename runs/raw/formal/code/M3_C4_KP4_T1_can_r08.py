import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 年化隐含波动率（小数表示）
r = 0.043       # 无风险利率（小数表示，连续复利）
T = 0.58        # 剩余期限（年）

# 1. 计算 d1 与 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. 按每单位波动率计算 vega (dC/dσ)
# vega = S * sqrt(T) * N'(d1)，其中 N'(x) 为标准正态分布的概率密度函数
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 4. 填充 result
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以供课堂展示
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print(f"欧式看涨期权价格 (Call Price) = {result['call_price']:.4f}")
print(f"看涨期权 Delta                = {result['call_delta']:.4f}")
print(f"看涨期权 Vega (每单位波动率)   = {result['call_vega']:.4f}")

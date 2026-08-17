import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7       # 标的资产当前价格
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（年化）
r = 0.043       # 无风险利率（连续复利）
T = 0.58        # 剩余期限（年）

# 1. 计算 d1 与 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 欧式看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 3. Delta = N(d1)
call_delta = norm.cdf(d1)

# 4. Vega (每单位波动率变化)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 5. 填充结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（供课堂展示）
print("计算结果：")
print(f"期权价格 (call_price) = {call_price:.6f}")
print(f"Delta (call_delta)    = {call_delta:.6f}")
print(f"Vega  (call_vega)     = {call_vega:.6f}")

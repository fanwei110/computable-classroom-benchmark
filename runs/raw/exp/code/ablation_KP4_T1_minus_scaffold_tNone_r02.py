import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# 设置参数
S = 103.7      # 当前股价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 27.6%
r = 0.043      # 无风险利率 4.3%
T = 0.58       # 剩余期限（年）

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 欧式看涨期权价格 (Black-Scholes公式)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta (看涨期权)
call_delta = norm.cdf(d1)

# Vega (每单位波动率变化)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 输出结果
print(f"期权价格: {call_price:.6f}")
print(f"Delta: {call_delta:.6f}")
print(f"Vega: {call_vega:.6f}")

# 按要求存入result字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 显示result字典内容
print("\nresult字典:")
for key, value in result.items():
    print(f"  '{key}': {value:.6f}")

# 验证结果并打印
print(f"\n验证:")
print(f"S*N(d1) = {S * norm.cdf(d1):.6f}")
print(f"K*e^(-rT)*N(d2) = {K * np.exp(-r * T) * norm.cdf(d2):.6f}")

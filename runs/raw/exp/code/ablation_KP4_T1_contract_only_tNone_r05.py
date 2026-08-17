import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# 定义参数
S = 103.7      # 当前股价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率（年化）
r = 0.043      # 无风险利率（年化）
T = 0.58       # 剩余期限（年）

# Black-Scholes 公式计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算 delta（看涨期权的 delta = N(d1)）
call_delta = norm.cdf(d1)

# 计算 vega（vega = S * sqrt(T) * N'(d1)）
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 输出结果
print(f"期权价格: {call_price:.6f}")
print(f"Delta: {call_delta:.6f}")
print(f"Vega: {call_vega:.6f}")

# 存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print("\n结果字典:")
print(result)

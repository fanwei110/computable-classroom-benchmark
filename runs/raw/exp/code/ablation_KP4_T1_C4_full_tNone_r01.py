import numpy as np
from scipy.stats import norm
# 如果不需要 pandas 和 matplotlib 可不用，但保留 import 以防后续扩展
import pandas as pd
import matplotlib.pyplot as plt

# 给定参数
S = 103.7        # 标的资产现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率 27.6% -> 小数
r = 0.043        # 无风险利率 4.3% -> 小数
T = 0.58         # 剩余期限（年）

# 步骤1：计算 d1 与 d2（连续复利）
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 步骤2：计算期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)      # 欧式看涨delta = N(d1)

# 步骤3：计算 vega（每单位波动率 dC/dσ）
# vega = S * N'(d1) * sqrt(T)
# 其中 N'(d1) = 1/sqrt(2π) * exp(-d1^2/2)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 步骤4：填充 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（保留足够精度以符合教学展示）
print("计算结果：")
print(f"期权价格 (call_price) = {result['call_price']:.6f}")
print(f"Delta (call_delta)     = {result['call_delta']:.6f}")
print(f"Vega  (call_vega)      = {result['call_vega']:.6f}")

# 如果需要查看字典原始值，可以直接 print(result)

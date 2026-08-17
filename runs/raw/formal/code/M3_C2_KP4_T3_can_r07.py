import numpy as np
from scipy.stats import norm

# ================== 参数设定 ==================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余期限（年）

# ================== 闭式解计算 ==================
# 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 计算希腊字母 Vega (期权价格对波动率的一阶偏导数)
# Vega 的闭式解为：Vega = S * N'(d1) * sqrt(T)
vega = S * norm.pdf(d1) * np.sqrt(T)

# ================== 推算价格响应 ==================
# 隐含波动率上升一个百分点，即变化量 d_sigma = 0.01
d_sigma = 0.01

# 利用 Vega 推算（一阶近似）期权价格对这一百分点波动率变化的响应
price_change = vega * d_sigma

# ================== 输出契约 ==================
result = {'price_change': price_change}

# (投屏展示用，输出结果以供核对)
print(f"d1 = {d1:.4f}")
print(f"Vega = {vega:.4f}")
print(f"波动率上升1%的价格响应 = {price_change:.4f}")
print(f"result = {result}")

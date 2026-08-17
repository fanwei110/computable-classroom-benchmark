import numpy as np
from scipy.stats import norm

# ==================== 已知参数 ====================
S = 103.7       # 股票现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (年化)
r = 0.043       # 无风险利率 (年化)
T = 0.58        # 剩余期限 (年)
q = 0.0         # 假设不分红，即股息率 q = 0

# ==================== 步骤 1: 计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 步骤 2: 计算期权价格与 Delta ====================
# 欧式看涨期权价格 (Black-Scholes 闭式解)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 看涨期权 Delta (不分红)
call_delta = norm.cdf(d1)

# ==================== 步骤 3: 计算 Vega ====================
# Vega: 期权价格对波动率的一阶偏导 (闭式解)
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# ==================== 步骤 4: 填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# (可选) 打印结果以便投屏展示
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"Call Price = {result['call_price']:.6f}")
print(f"Call Delta = {result['call_delta']:.6f}")
print(f"Call Vega  = {result['call_vega']:.6f}")

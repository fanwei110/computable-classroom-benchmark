import numpy as np
from scipy.stats import norm

# ---------------- 市场参数 ----------------
S = 103.7       # 标的资产价格
K = 97.5        # 行权价
sigma = 0.276   # 波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余到期时间 (年)
q = 0.0         # 股息率 (题目说明不分红)

# ---------------- 步骤 1: 计算 d1 与 d2 ----------------
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ---------------- 步骤 2: 计算期权价格与 delta ----------------
# 欧式看涨期权价格 (Black-Scholes 公式)
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 Delta
call_delta = np.exp(-q * T) * norm.cdf(d1)

# ---------------- 步骤 3: 计算 vega ----------------
# Vega (对波动率的一阶偏导)，注意此处为数学定义的绝对值，即 vol 变动 1.0 (100%) 对应的价格变动
# 若习惯看 vol 变动 1% 的价格变动，通常将此值乘以 0.01
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# ---------------- 步骤 4: 填充 result ----------------
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 课堂投屏展示
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"Call Price = {result['call_price']:.4f}")
print(f"Call Delta = {result['call_delta']:.4f}")
print(f"Call Vega  = {result['call_vega']:.4f}")
print("-" * 30)
print("result dict:", result)

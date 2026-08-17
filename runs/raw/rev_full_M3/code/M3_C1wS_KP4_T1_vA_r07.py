import numpy as np
from scipy.stats import norm

# === 参数设定 ===
S = 103.7       # 标的现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余期限 (年)
q = 0.0         # 股息率 (不分红)

# === 步骤1：计算 d1 与 d2 ===
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# === 步骤2：计算期权价格与 delta ===
# 求解标准正态分布累积概率
N_d1 = norm.cdf(d1)
N_d2 = norm.cdf(d2)

# 欧式看涨期权价格公式: C = S * e^(-qT) * N(d1) - K * e^(-rT) * N(d2)
call_price = S * np.exp(-q * T) * N_d1 - K * np.exp(-r * T) * N_d2

# 看涨期权 Delta 公式: Delta = e^(-qT) * N(d1)
call_delta = np.exp(-q * T) * N_d1

# === 步骤3：计算 vega ===
# 求解标准正态分布概率密度
n_d1 = norm.pdf(d1)

# Vega 公式: Vega = S * e^(-qT) * n(d1) * sqrt(T)
# 注：此处为数学导数 dC/dsigma，表示波动率每变动1单位(100%)的价格变动量。
# 市场惯例常报出波动率每变动1%的价格变动，即 Vega/100。
call_vega = S * np.exp(-q * T) * n_d1 * np.sqrt(T)

# === 步骤4：填充 result ===
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# ---- 课堂投屏辅助打印 (可忽略，仅为展示) ----
print("="*45)
print(" Black-Scholes 欧式看涨期权计算结果")
print("="*45)
print(f"  d1         = {d1:.6f}")
print(f"  d2         = {d2:.6f}")
print(f"  N(d1)      = {N_d1:.6f}")
print(f"  N(d2)      = {N_d2:.6f}")
print(f"  n(d1)      = {n_d1:.6f}")
print("-" * 45)
print(f"  Call Price = {call_price:.4f}")
print(f"  Call Delta = {call_delta:.4f}")
print(f"  Call Vega  = {call_vega:.4f}  (dC/dσ)")
print(f"  Vega(1%)   = {call_vega/100:.4f}  (波动率每变动1%的价格变动)")
print("="*45)

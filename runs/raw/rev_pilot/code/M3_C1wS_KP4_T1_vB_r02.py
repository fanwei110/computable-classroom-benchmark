import numpy as np
from scipy.stats import norm

# ============ 参数 ============
S = 103.7       # 标的资产价格
K = 97.5        # 行权价
sigma = 0.276   # 波动率 27.6%
r = 0.043       # 无风险利率 4.3%
T = 0.58        # 剩余到期时间（年）
q = 0.0         # 连续股息率（不分红）

# ============ Step 1: 计算 d1 与 d2 ============
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ============ Step 2: 计算期权价格与 delta ============
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)

# ============ Step 3: 计算 vega ============
# vega = dC/d(sigma)，每单位波动率变动对应的期权价格变动
call_vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)

# ============ Step 4: 填充 result ============
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# ============ 输出 ============
print("=" * 55)
print("  欧式看涨期权 Black-Scholes 定价与希腊字母")
print("=" * 55)
print(f"  标的 S = {S}    行权 K = {K}")
print(f"  波动率 σ = {sigma*100:.1f}%   利率 r = {r*100:.1f}%")
print(f"  期限 T = {T} 年   股息率 q = {q*100:.1f}%")
print("-" * 55)
print(f"  d1 = {d1:.6f}")
print(f"  d2 = {d2:.6f}")
print("-" * 55)
print(f"  Call Price = {call_price:.4f}")
print(f"  Call Delta  = {call_delta:.6f}")
print(f"  Call Vega   = {call_vega:.4f}  (每单位σ变动)")
print(f"  Call Vega   = {call_vega/100:.4f}  (每1%σ变动)")
print("=" * 55)

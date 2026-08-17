import numpy as np
from scipy.stats import norm

# =====================
# 1. 定义输入参数
# =====================
S = 103.7       # 股票现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (年化，27.6%)
r = 0.043       # 无风险利率 (年化，4.3%)
T = 0.58        # 剩余期限 (年)

# =====================
# 2. 计算 d1 与 d2
# =====================
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# =====================
# 3. 计算期权价格与 delta
# =====================
# 欧式看涨期权价格 C = S * N(d1) - K * exp(-rT) * N(d2)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 看涨期权 delta = N(d1)
call_delta = norm.cdf(d1)

# =====================
# 4. 计算 vega
# =====================
# Vega = dC/d(sigma) = S * sqrt(T) * N'(d1)
# 注：此为对波动率求导的纯数学值；若需表示波动率每变动1%的价格变化，业界常再乘以0.01
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# =====================
# 5. 填充 result 字典
# =====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# (可选) 输出中间过程与结果，便于课堂展示与核对
print(f"--- 中间变量 ---")
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print(f"\n--- 计算结果 ---")
print(f"Call Price = {call_price:.6f}")
print(f"Call Delta = {call_delta:.6f}")
print(f"Call Vega   = {call_vega:.6f}")
print(f"\n--- 输出契约字典 ---")
print(result)

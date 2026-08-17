import numpy as np
from scipy.stats import norm

# ================= 基础参数设定 =================
S = 103.7       # 标的现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余到期时间 (年)
q = 0.0         # 股息率 (题目未指明分红，假设为0)

# ================= 步骤 1：计算 d1 与 d2 =================
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ================= 步骤 2：计算期权价格与 delta =================
# 欧式看涨期权价格 (Black-Scholes-Merton 闭式解)
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 Delta
call_delta = np.exp(-q * T) * norm.cdf(d1)

# ================= 步骤 3：计算 vega =================
# Vega (对波动率的一阶偏导)，注意此处为绝对值，即波动率变化1个单位(100%)对应的价格变化
# 部分交易惯例会除以100(即波动率变化1%对应的价格变化)，此处按数学严格定义给出
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# ================= 步骤 4：填充 result =================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以供课堂投屏验证
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"Call Price = {result['call_price']:.6f}")
print(f"Call Delta = {result['call_delta']:.6f}")
print(f"Call Vega  = {result['call_vega']:.6f}")

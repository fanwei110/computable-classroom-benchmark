import numpy as np
from scipy.stats import norm

# ---------- 输入参数 ----------
S = 103.7        # 标的资产当前价格
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率（27.6%）
r = 0.043        # 无风险利率（4.3%）
T = 0.58         # 剩余期限（年）

# ---------- Black-Scholes 闭式解（欧式看涨期权） ----------
# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = norm.cdf(d1)

# Vega（单位：每单位波动率，即 dC/dσ）
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# ---------- 输出 ----------
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果（便于课堂展示）
print("欧式看涨期权定价结果：")
print(f"价格    = {call_price:.6f}")
print(f"Delta   = {call_delta:.6f}")
print(f"Vega    = {call_vega:.6f}")

import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7       # 股票现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（年化，小数表示）
r = 0.043       # 无风险利率（连续复利，小数表示）
T = 0.58        # 剩余期限（年）

# ==================== 步骤1：计算 d1 与 d2 ====================
# 根据Black-Scholes公式，对于无分红股票：
# d1 = [ln(S/K) + (r + 0.5*sigma^2)*T] / (sigma*sqrt(T))
# d2 = d1 - sigma*sqrt(T)
sigma_sqrt_T = sigma * np.sqrt(T)

d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / sigma_sqrt_T
d2 = d1 - sigma_sqrt_T

# ==================== 步骤2：计算期权价格与 delta ====================
# 看涨期权价格 C = S*N(d1) - K*exp(-rT)*N(d2)
# 看涨期权 delta = N(d1)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# ==================== 步骤3：计算 vega ====================
# vega = dC/dσ = S * N'(d1) * sqrt(T)
# 其中 N'(d1) 是标准正态分布的概率密度函数(pdf)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# ==================== 步骤4：填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 课堂投屏展示结果
print(f"Black-Scholes 欧式看涨期权计算结果：")
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"期权价格 = {result['call_price']:.4f}")
print(f"Delta (Δ) = {result['call_delta']:.6f}")
print(f"Vega (ν)  = {result['call_vega']:.4f}")

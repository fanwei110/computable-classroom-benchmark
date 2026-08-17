import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (年化，小数表示)
r = 0.043       # 无风险利率 (连续复利，小数表示)
T = 0.58        # 剩余期限 (年)
q = 0.0         # 股息率 (不分红股票，故为0)

# ==================== 计算步骤 ====================

# 1. 用连续复利利率计算 d1 与 d2
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格与 delta = N(d1)
# 欧式看涨期权定价公式: C = S * e^(-qT) * N(d1) - K * e^(-rT) * N(d2)
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 对于无分红资产，看涨期权 Delta = e^(-qT) * N(d1) = N(d1)
call_delta = np.exp(-q * T) * norm.cdf(d1)

# 3. 按每单位波动率计算 vega（dC/dσ），用小数表示
# 对于无分红资产，Vega = S * e^(-qT) * N'(d1) * sqrt(T)
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# 4. 填充 result
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果以便课堂展示验证
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print(f"欧式看涨期权价格 (Call Price) = {result['call_price']:.4f}")
print(f"看涨期权 Delta               = {result['call_delta']:.4f}")
print(f"看涨期权 Vega (每单位波动率)   = {result['call_vega']:.4f}")

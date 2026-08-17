import numpy as np
from scipy.stats import norm

# =====================
// 1. 参数设置
// =====================
S = 103.7      # 股票现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (年化，即27.6%)
r = 0.043      # 无风险利率 (年化，即4.3%)
T = 0.58       # 剩余期限 (年)
# 题目明确为不分红股票，因此股息收益率 q = 0

# =====================
// 2. 计算 d1 与 d2
// =====================
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# =====================
// 3. 计算期权价格与 delta
// =====================
# 欧式看涨期权价格 (Black-Scholes 闭式解)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 看涨期权 delta
call_delta = norm.cdf(d1)

# =====================
// 4. 计算 vega
// =====================
# Vega 的标准数学定义为对波动率 sigma 的偏导数：∂C/∂σ = S * sqrt(T) * N'(d1)
# 注：部分实务场景中会报告波动率每变动1%的影响(即乘以0.01)，此处采用严格的数学偏导数定义
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# =====================
// 5. 填充 result 字典
// =====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# (可选) 课堂展示打印，方便直观查看
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"Call Price = {call_price:.6f}")
print(f"Call Delta = {call_delta:.6f}")
print(f"Call Vega  = {call_vega:.6f}")
print("-" * 30)
print("Result Dictionary:")
print(result)

import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (年化)
r = 0.043       # 无风险利率 (年化)
T = 0.58        # 剩余期限 (年)

# 步骤 1: 计算 d1 与 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 步骤 2: 计算期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 步骤 3: 计算 vega
# vega 是期权价格对波动率的偏导数 dC/dsigma
# 注：按金融实务，若需表示波动率每变动1%对价格的影响，需将此结果除以100
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 步骤 4: 填充 result
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 课堂投屏展示辅助信息
print(f"===== 中间计算过程 =====")
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print(f"\n===== 期权价格与希腊字母 =====")
print(f"Call Price = {call_price:.6f}")
print(f"Call Delta = {call_delta:.6f}")
print(f"Call Vega  = {call_vega:.6f}")
print(f"\n===== 最终输出字典 =====")
print(result)

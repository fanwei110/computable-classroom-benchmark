import numpy as np
from scipy.stats import norm
import json

# 输入参数
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（年化）
T = 0.58        # 剩余期限（年）
r = 0.043       # 无风险利率（年化）

# 第一步：计算 d1 和 d2
d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")

# 第二步：计算期权价格和Delta
# N(d1) 和 N(d2) 是标准正态分布的累积分布函数
Nd1 = norm.cdf(d1)
Nd2 = norm.cdf(d2)

# 实现欧式看涨期权定价模型
call_price = S * Nd1 - K * np.exp(-r * T) * Nd2

# Delta = N(d1)（对于看涨期权）
call_delta = Nd1

print(f"期权价格 = {call_price:.6f}")
print(f"Delta = {call_delta:.6f}")

# 第三步：计算 Vega
# Vega = S * sqrt(T) * N'(d1)，其中 N'(d1) 是标准正态分布的概率密度函数
# 注意：Vega通常以每1%波动率变化的价格变化来表示
N_prime_d1 = norm.pdf(d1)
vega = S * np.sqrt(T) * N_prime_d1

# 将Vega标准化为每1%波动率变化（除以100）
call_vega = vega / 100

print(f"标准化后Vega（每1%波动率变化）= {call_vega:.6f}")

# 输出结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印标准化Vega的解释
print(f"\nVega解释：波动率每变化1个百分点（如从27.6%到28.6%或26.6%），期权价格变动约 {call_vega:.6f} 货币单位")

# 打印结果
print("\n结果字典：")
print(json.dumps(result, indent=2))

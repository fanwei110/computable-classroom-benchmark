import numpy as np
from scipy.stats import norm

"""
Black-Scholes 期权定价与希腊字母计算
计算隐含波动率上升一个百分点对欧式看涨期权价格的影响
"""

# 给定参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)
delta_sigma = 0.01  # 波动率变化 (一个百分点)

# Black-Scholes 公式相关计算
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算 vega: 期权价格对波动率的导数
# vega = S * sqrt(T) * N'(d1)
# 其中 N'(d1) 是标准正态分布的概率密度函数
vega = S * np.sqrt(T) * norm.pdf(d1)

# 波动率上升一个百分点导致的价格变化
# 注意 vega 通常以波动率每变化1个百分点(0.01)来报价
# 所以价格变化 = vega * delta_sigma
price_change = vega * delta_sigma

# 将结果存入 result 字典
result = {
    'price_change': price_change
}

# 输出结果
print("=" * 60)
print("Black-Scholes 期权定价 - Vega 计算")
print("=" * 60)
print(f"标的资产现价 (S): {S}")
print(f"行权价 (K): {K}")
print(f"波动率 (σ): {sigma*100:.1f}%")
print(f"无风险利率 (r): {r*100:.1f}%")
print(f"剩余期限 (T): {T} 年")
print(f"波动率变化 (Δσ): {delta_sigma*100:.0f} 个百分点")
print("-" * 60)
print(f"d1: {d1:.6f}")
print(f"d2: {d2:.6f}")
print(f"N'(d1): {norm.pdf(d1):.6f}")
print(f"Vega: {vega:.6f}")
print("-" * 60)
print(f"期权价格变化: {price_change:.6f}")
print("=" * 60)
print(f"\nresult = {result}")

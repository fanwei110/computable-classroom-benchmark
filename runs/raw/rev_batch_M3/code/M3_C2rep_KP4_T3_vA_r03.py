import numpy as np
from scipy.stats import norm

# ==================== 已知参数 ====================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余期限 (年)

# ==================== 计算过程 ====================
# 1. 计算 Black-Scholes 模型中的 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 2. 计算欧式看涨期权的 Vega (Vega = S * N'(d1) * sqrt(T))
# 其中 N'(d1) 为标准正态分布的概率密度函数(PDF)
vega = S * norm.pdf(d1) * np.sqrt(T)

# 3. 推算期权价格对这一个百分点波动率变化的响应
# 隐含波动率上升一个百分点，即 Delta_sigma = 1% = 0.01
# 由泰勒展开一阶项：Delta_C ≈ Vega * Delta_sigma
delta_sigma = 0.01
price_change = vega * delta_sigma

# ==================== 输出契约 ====================
result = {
    'price_change': price_change
}

# （投屏辅助打印，非必须但有助于课堂展示）
print(f"--- Black-Scholes 希腊字母计算 ---")
print(f"d1 = {d1:.4f}")
print(f"Vega = {vega:.4f}")
print(f"波动率上升1%导致的期权价格变化 = {price_change:.4f}")
print(f"\n输出结果字典: {result}")

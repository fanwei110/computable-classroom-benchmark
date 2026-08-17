import numpy as np
from scipy.stats import norm

# ==========================================
# 欧式期权 Black-Scholes 模型与希腊字母计算
# ==========================================

# 1. 已知参数与假设设定
S = 103.7       # 标的资产价格
K = 97.5        # 行权价
sigma = 0.276   # 波动率 (年化，27.6%)
r = 0.043       # 无风险利率 (年化，4.3%)
T = 0.58        # 到期时间 (年)
d_sigma = 0.01  # 隐含波动率(IV)上涨1个百分点 (即 0.01)

# 假设处理：
# - 题目未指明期权类型(看涨/看跌)与股息率。由于看涨与看跌欧式期权的 Vega 完全相等，
#   因此无需指明期权类型即可计算价格对波动率的响应。
# - 未指明股息率，采用连续股息率 q = 0 的标准假设。

# 2. 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 3. 计算标准正态分布的概率密度函数 N'(d1)
nd1 = norm.pdf(d1)

# 4. 计算 Vega (数学定义：Vega = dC / d_sigma)
# 对于无股息欧式期权，Vega = S * N'(d1) * sqrt(T)
vega = S * nd1 * np.sqrt(T)

# 5. 推算期权价格对 1 个百分点波动率变化的响应
# 由于 Vega 是期权价格对波动率的一阶导数，当 IV 变化 d_sigma = 0.01 时：
price_change = vega * d_sigma

# 6. 按照输出契约存入 result 字典
result = {
    'price_change': price_change
}

# ==========================================
# 课堂投屏辅助输出 (便于验证计算过程)
# ==========================================
print("="*50)
print("《证券投资学》- Black-Scholes 希腊字母 Vega 计算")
print("="*50)
print(f"输入参数: S={S}, K={K}, sigma={sigma*100}%, r={r*100}%, T={T}年")
print(f"d1 计算值: {d1:.4f}")
print(f"N'(d1) 值: {nd1:.4f}")
print(f"数学 Vega (每1.0波动率变化): {vega:.4f}")
print(f"IV 涨 1 个百分点(0.01)导致的价格变化: {price_change:.4f}")
print("-" * 50)
print(f"最终结果 result: {result}")
print("="*50)

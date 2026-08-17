import numpy as np
from scipy.stats import norm

# ===== 1. 参数设置 =====
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 初始波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余到期时间（年）

# ===== 2. 计算希腊字母 Vega =====
# 计算 d1 的闭式解
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 计算 Vega (期权价格对波动率的一阶偏导数)
# Vega = S * N'(d1) * sqrt(T)，其中 N' 为标准正态分布的概率密度函数
vega = S * norm.pdf(d1) * np.sqrt(T)

# ===== 3. 推算价格变化 =====
# 隐含波动率上升一个百分点，即波动率绝对值变化 0.01
delta_sigma = 0.01

# 利用希腊字母 Vega 推算期权价格对这1%波动率变化的响应（一阶线性近似）
price_change = vega * delta_sigma

# ===== 4. 保存结果 =====
result = {
    'price_change': price_change
}

# 输出结果以供投屏演示验证
print(f"布莱克-斯科尔斯框架下：")
print(f"d1 = {d1:.4f}")
print(f"Vega = {vega:.4f}")
print(f"波动率上升1%时期权价格变化推算值 = {price_change:.4f}")
print(f"\n最终结果字典: {result}")

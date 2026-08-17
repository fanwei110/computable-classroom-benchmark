import numpy as np
from scipy.stats import norm

# ====================
// 1. 参数设定
# ====================
S = 103.7       # 标的资产价格
K = 97.5        # 行权价
sigma = 0.276   # 波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余期限 (年)

# ====================
// 2. 计算 Black-Scholes 模型中的 d1
# ====================
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

# ====================
// 3. 计算欧式期权的 Vega
# ====================
# 注：根据BS闭式解，看涨与看跌期权的 Vega 完全相同，公式为 S * N'(d1) * sqrt(T)
vega = S * norm.pdf(d1) * np.sqrt(T)

# ====================
// 4. 推算期权价格对这一个百分点波动率变化的响应
# ====================
# 隐含波动率上涨1个百分点，即波动率变化量 delta_sigma = 0.01
# 期权价格的一阶变化响应近似为：Delta_Price ≈ Vega * delta_sigma
delta_sigma = 0.01
price_change = vega * delta_sigma

# ====================
// 5. 按输出契约存储结果
# ====================
result = {'price_change': price_change}

# 课堂展示辅助打印（方便教师投屏讲解）
print(f"--- Black-Scholes 希腊字母计算 ---")
print(f"d1            : {d1:.6f}")
print(f"Vega (每1.0)  : {vega:.6f}")
print(f"波动率增加1%  : 价格变化响应为 {price_change:.6f}")

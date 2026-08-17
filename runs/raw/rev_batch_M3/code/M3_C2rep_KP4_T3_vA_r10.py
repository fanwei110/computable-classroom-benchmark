import numpy as np
from scipy.stats import norm

# ==========================================
# 欧式看涨期权 Black-Scholes 模型与希腊字母
# ==========================================

# 1. 已知参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# 2. 计算 d1
# 闭式解公式: d1 = [ln(S/K) + (r + 0.5 * sigma^2) * T] / (sigma * sqrt(T))
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 3. 计算 Vega (对波动率的一阶导数)
# 闭式解公式: Vega = S * sqrt(T) * N'(d1)，其中 N'(d1) 为标准正态分布的概率密度函数
vega = S * np.sqrt(T) * norm.pdf(d1)

# 4. 推算波动率上升一个百分点 (1% = 0.01) 时的期权价格变化
# 利用希腊字母的一阶近似: ΔPrice ≈ Vega * Δσ
delta_sigma = 0.01
price_change = vega * delta_sigma

# 5. 将结果存入字典，键名严格为 'price_change'
result = {
    'price_change': price_change
}

# ==========================================
# 课堂展示输出 (可选，便于投屏观察)
# ==========================================
print(f"--- Black-Scholes 欧式看涨期权分析 ---")
print(f"标的现价: {S}, 行权价: {K}, 波动率: {sigma*100}%, 利率: {r*100}%, 剩余期限: {T}年")
print(f"d1 计算值: {d1:.4f}")
print(f"Vega 计算值: {vega:.4f}")
print(f"隐含波动率上升 1% 时，推算的期权价格变化量: {price_change:.4f}")
print(f"result字典内容: {result}")

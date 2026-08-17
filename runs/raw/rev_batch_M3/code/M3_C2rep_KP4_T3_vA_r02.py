import numpy as np
from scipy.stats import norm

# ==========================================
# 欧式看涨期权 Black-Scholes 定价与希腊字母
# ==========================================

# 已知参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 波动率 27.6%
r = 0.043      # 无风险利率 4.3%
T = 0.58       # 剩余期限（年）
delta_sigma = 0.01  # 隐含波动率上升一个百分点（1%）

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算期权价格 (闭式解，供参考验证)
C = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算 Vega (闭式解)
# Vega 的数学定义为 dC/dsigma，即波动率变化 1 个单位(100%)时价格的变化量
# 公式为：Vega = S * norm.pdf(d1) * sqrt(T)
vega = S * norm.pdf(d1) * np.sqrt(T)

# 推算期权价格对这一个百分点(1%)波动率变化的响应
# 根据泰勒一阶展开，当波动率变化 dsigma 时，价格变化 dC ≈ Vega * dsigma
price_change = vega * delta_sigma

# 按照输出契约，存储结果到字典
result = {
    'price_change': price_change
}

# 以下为课堂投屏展示辅助打印
print("="*45)
print(" Black-Scholes 欧式看涨期权与希腊字母分析")
print("="*45)
print(f" 标的现价 (S)     : {S}")
print(f" 行权价   (K)     : {K}")
print(f" 当前波动率(sigma): {sigma*100:.1f}%")
print(f" 无风险利率 (r)   : {r*100:.1f}%")
print(f" 剩余期限 (T)     : {T} 年")
print("-"*45)
print(f" 计算得 d1        : {d1:.4f}")
print(f" 计算得 d2        : {d2:.4f}")
print(f" 期权当前价格 (C) : {C:.4f}")
print(f" 期权 Vega        : {vega:.4f}")
print("-"*45)
print(f" 情景：隐含波动率上升 1 个百分点 (Δσ = {delta_sigma})")
print(f" 推算期权价格响应 : {price_change:.4f}")
print("="*45)

# 打印最终结果字典
print(f"\n输出契约结果: {result}")

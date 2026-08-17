import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7        # 标的资产现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率 (年化)
r = 0.043        # 无风险利率 (年化)
T = 0.58         # 剩余期限 (年)

# ==================== 步骤1：计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 步骤2：计算期权价格与 delta ====================
# 欧式看涨期权价格 C = S * N(d1) - K * exp(-rT) * N(d2)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 Delta = N(d1)
call_delta = norm.cdf(d1)

# ==================== 步骤3：计算 vega ====================
# Vega = S * sqrt(T) * N'(d1)，其中 N'(d1) 为标准正态分布的概率密度函数
# 注：此处 Vega 为价格对波动率的偏导数（绝对值），表示波动率变动1单位（即100%）时期权价格的变化量。
# 若需表示波动率变动1%时的价格变化，通常将此值除以100。
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# ==================== 步骤4：填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 课堂投屏展示辅助输出
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"欧式看涨期权价格 (Call Price) = {result['call_price']:.4f}")
print(f"看涨期权 Delta               = {result['call_delta']:.6f}")
print(f"看涨期权 Vega                = {result['call_vega']:.4f}")
print("-" * 30)
print("result 字典已生成。")

import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (年化，27.6%)
r = 0.043      # 无风险利率 (年化，4.3%)
T = 0.58       # 剩余期限 (年)

# ==================== 计算步骤 ====================

# 1. 计算 d1 与 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格与 delta
# 看涨期权价格 C = S * N(d1) - K * exp(-rT) * N(d2)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 看涨期权 delta = N(d1)
call_delta = norm.cdf(d1)

# 3. 计算 vega
# vega = S * sqrt(T) * N'(d1)，其中 N'(x) 为标准正态分布的概率密度函数
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# ==================== 填充结果 ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以便投屏展示
for key, value in result.items():
    print(f"{key}: {value:.6f}")

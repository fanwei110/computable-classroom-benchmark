import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7       # 标的价格
K = 97.5        # 行权价
T = 0.58        # 剩余时间（年）
r = 0.043       # 无风险利率
sigma = 0.276   # 波动率

# 计算d1和d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算Call价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算Delta
call_delta = norm.cdf(d1)

# 计算Vega（注意：Vega的单位是每1%波动率变化对应的价格变化，因此需要乘以0.01）
call_vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01

# 存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

result

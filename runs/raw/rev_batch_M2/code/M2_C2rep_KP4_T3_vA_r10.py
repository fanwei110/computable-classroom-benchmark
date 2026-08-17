import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7       # 标的现价
K = 97.5        # 行权价
sigma = 0.276   # 波动率（27.6%）
r = 0.043       # 无风险利率（4.3%）
T = 0.58        # 剩余时间（年）

# 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# Vega：波动率每变动1单位（100个百分点）对应的价格变化
vega = S * np.sqrt(T) * norm.pdf(d1)

# 隐含波动率上升1个百分点（0.01）对应的价格变化
price_change = vega * 0.01

# 按输出契约存入字典
result = {'price_change': price_change}

# 打印结果（供课堂投屏验证）
print(result)

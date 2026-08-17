import numpy as np
from scipy.stats import norm

# 给定参数
S0 = 103.7       # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率（小数形式）
r = 0.043        # 无风险利率
T = 0.58         # 剩余期限（年）

# 计算 d1
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 计算 Vega（期权价格对波动率的偏导数）
# Vega = S0 * N'(d1) * sqrt(T)，这是波动率变动1单位（即100%）时的价格变动
vega = S0 * norm.pdf(d1) * np.sqrt(T)

# 波动率上升一个百分点（即 sigma 增加 0.01）对应的价格变化
price_change = vega * 0.01

# 按要求的格式存入 result 字典
result = {'price_change': price_change}

# 可选：输出结果以供检查
print(result)

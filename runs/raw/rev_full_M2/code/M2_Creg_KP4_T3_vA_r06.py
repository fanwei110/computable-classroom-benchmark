import numpy as np
from scipy.stats import norm

# 给定的参数
S = 103.7        # 标的资产现价
K = 97.5         # 行权价
sigma = 0.276    # 波动率 (27.6%)
r = 0.043        # 无风险利率 (4.3%)
T = 0.58         # 剩余时间 (年)

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 标准正态概率密度函数在 d1 处的值
phi_d1 = norm.pdf(d1)

# Vega: 期权价格对波动率的偏导数 (波动率为小数形式)
vega = S * np.sqrt(T) * phi_d1

# 隐含波动率上升一个百分点（即 0.01），期权价格的变动
delta_sigma = 0.01
price_change = vega * delta_sigma

# 按输出契约存入字典
result = {
    'price_change': price_change
}

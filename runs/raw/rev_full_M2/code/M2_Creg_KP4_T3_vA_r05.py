import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 当前隐含波动率
r = 0.043          # 无风险利率
T = 0.58           # 剩余年限

# 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

# Vega：波动率（小数形式）每变动 1 单位，期权价格的变动量
vega = S * np.sqrt(T) * norm.pdf(d1)

# 隐含波动率上升一个百分点（即从 27.6% 到 28.6%，Δσ = 0.01）
price_change = vega * 0.01

# 输出契约
result = {'price_change': price_change}
print(result)

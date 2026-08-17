import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# 输入参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 波动率（小数形式）
r = 0.043          # 无风险利率
T = 0.58           # 剩余期限（年）
delta_sigma = 0.01 # 隐含波动率上升一个百分点

# 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 计算 Vega（对波动率小数的导数）
# Vega = S * N'(d1) * sqrt(T)
vega = S * norm.pdf(d1) * np.sqrt(T)

# 隐含波动率上升一个百分点带来的期权价格变化
# 注意：Vega 对小数波动率的导数是 vega，
# 波动率上升 0.01，价格变化 = vega * 0.01
price_change = vega * delta_sigma

# 存入结果字典
result = {
    'price_change': price_change
}

# 打印结果
print(result)

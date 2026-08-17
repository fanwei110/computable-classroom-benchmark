import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7           # 标的现价
K = 97.5            # 行权价
sigma = 0.276       # 隐含波动率（27.6%）
r = 0.043           # 无风险利率（4.3%）
T = 0.58            # 剩余期限（年）
delta_sigma = 0.01  # 波动率上升一个百分点

# Black-Scholes 公式中的 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

# Vega：期权价格对波动率（小数）的偏导数
vega = S * np.sqrt(T) * norm.pdf(d1)

# 波动率上升 0.01 带来的价格变化
price_change = vega * delta_sigma

# 严格按照要求输出
result = {
    'price_change': price_change
}

print(result)

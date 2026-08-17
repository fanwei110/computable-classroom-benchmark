import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7        # 标的资产价格
K = 97.5         # 行权价
T = 0.58         # 剩余期限（年）
r = 0.043        # 无风险利率
sigma = 0.276    # 波动率

# 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# vega（波动率每变动 1 单位（即 100%）时的价格变动）
# 标准 Black-Scholes vega = S * sqrt(T) * N'(d1)
vega = S * np.sqrt(T) * norm.pdf(d1)

# 波动率上涨 1 个百分点，即 sigma 增加 0.01
price_change = vega * 0.01

# 存储结果
result = {
    'price_change': price_change
}

print(result)

import numpy as np
from scipy.stats import norm

# 输入参数
S0 = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276

# 计算 d1
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# 计算 N'(d1)
N_prime_d1 = norm.pdf(d1)

# 计算 Vega
vega = S0 * np.sqrt(T) * N_prime_d1

# 波动率变化 1% 对应的期权价格变化
price_change = vega * 0.01

# 存入结果
result = {
    'price_change': price_change
}

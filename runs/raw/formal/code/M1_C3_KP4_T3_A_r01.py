import numpy as np
from scipy.stats import norm

# 参数
S0 = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma = 0.276

# 计算d1
d1 = (np.log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))

# 计算N'(d1)
N_prime_d1 = norm.pdf(d1)

# 计算Vega
vega = S0 * np.sqrt(T) * N_prime_d1

# 波动率变化1%对期权价格的影响
price_change = vega * 0.01

# 存入结果字典
result = {
    'price_change': price_change
}

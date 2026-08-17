import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 年化隐含波动率
r = 0.043          # 年化无风险利率
T = 0.58           # 剩余期限（年）

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 欧式看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = norm.cdf(d1)

# Vega：波动率每变动 1 个百分点（0.01）引起的期权价格变动
# 标准 Black-Scholes vega = S * N'(d1) * sqrt(T) * 0.01
call_vega = S * norm.pdf(d1) * np.sqrt(T) * 0.01

# 结果汇总
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

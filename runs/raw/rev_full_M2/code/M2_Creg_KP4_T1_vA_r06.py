import numpy as np
from scipy.stats import norm

# 市场参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 年化隐含波动率
r = 0.043          # 无风险利率
T = 0.58           # 剩余期限（年）

# Black-Scholes 中间变量
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 欧式看涨期权价格、Delta、Vega
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega = S * norm.pdf(d1) * np.sqrt(T)    # 波动率每变化1（即100%）的敏感度

# 输出契约：将所有结果存入字典 result
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

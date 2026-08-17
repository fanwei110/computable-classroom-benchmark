import numpy as np
from scipy.stats import norm

# 已知参数
S = 103.7      # 标的现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率
r = 0.043      # 无风险利率（连续复利）
T = 0.58       # 到期时间（年）

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算欧式看涨期权价格
# C = S * N(d1) - K * exp(-rT) * N(d2)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算 Delta
# Delta = N(d1)
call_delta = norm.cdf(d1)

# 计算 Vega
# Vega = S * N'(d1) * sqrt(T)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 构建结果字典
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print(result)

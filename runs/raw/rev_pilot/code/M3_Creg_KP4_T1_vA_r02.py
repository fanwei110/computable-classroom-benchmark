import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7       # 股票现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（年化）
r = 0.043       # 无风险利率（年化）
T = 0.58        # 剩余期限（年）

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算欧式看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算 Delta (dC/dS)
call_delta = norm.cdf(d1)

# 计算 Vega (dC/dsigma)
# 注：此处采用数学标准定义，即波动率变化 1.0 (100%) 对应的期权价格变化。
# 若需波动率变化 1% 对应的价格变化，可再除以 100。
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 将结果存入要求的字典中
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以供验证
print(result)

import numpy as np
from scipy.stats import norm

# ----- 给定参数 -----
S = 103.7       # 股票现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（年化）
r = 0.043       # 无风险利率（连续复利）
T = 0.58        # 剩余期限（年）
q = 0.0         # 不分红股票

# ----- 1. 计算 d1 与 d2 -----
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ----- 2. 计算期权价格与 delta -----
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)  # 对不分红股票即为 N(d1)

# ----- 3. 计算 vega（每单位波动率的变化） -----
# vega = S * sqrt(T) * N'(d1) * exp(-q*T), 对于 q=0 即为 S*sqrt(T)*N'(d1)
call_vega = S * np.sqrt(T) * norm.pdf(d1) * np.exp(-q * T)

# ----- 4. 填充结果字典 -----
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果，便于课堂投屏查看
print(result)

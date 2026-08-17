import numpy as np
from scipy.stats import norm

# 期权参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# Black-Scholes公式计算d1和d2
d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 期权价格 (欧式看涨期权)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = norm.cdf(d1)

# Vega (每波动1个百分点，即0.01)
call_vega = S * norm.pdf(d1) * np.sqrt(T) * 0.01  # 标准化为每1%波动率变化

# 存入结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果
print(f"Call Price: {result['call_price']:.4f}")
print(f"Call Delta: {result['call_delta']:.4f}")
print(f"Call Vega: {result['call_vega']:.4f}")

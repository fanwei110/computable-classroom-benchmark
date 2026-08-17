import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7      # 标的价格
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# Black-Scholes 欧式看涨期权定价公式
# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = norm.cdf(d1)

# Vega (每单位波动率，即 dC/dσ)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 将结果存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 按教师要求输出结果（保留足够精度）
print("期权价格:", result['call_price'])
print("看涨 Delta:", result['call_delta'])
print("看涨 Vega:", result['call_vega'])

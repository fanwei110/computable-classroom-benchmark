import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7        # 标的资产现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率 (27.6%)
r = 0.043        # 无风险利率 (4.3%)
T = 0.58         # 剩余期限 (年)

# 1. 计算 d1 与 d2 (Black-Scholes 公式)
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 期权价格 (欧式看涨)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 3. Delta = N(d1)
call_delta = norm.cdf(d1)

# 4. Vega (每单位波动率变化引起的价格变化, 小数表示)
#    vega = S * sqrt(T) * n(d1) , 其中 n(x) 是标准正态密度函数
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 5. 存入 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（供课堂演示）
print("期权价格 (call_price):", result['call_price'])
print("Delta (call_delta):", result['call_delta'])
print("Vega (call_vega):", result['call_vega'])

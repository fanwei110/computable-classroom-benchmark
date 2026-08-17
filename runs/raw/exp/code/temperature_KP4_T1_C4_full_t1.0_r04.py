import numpy as np
from scipy.stats import norm

# 给定的参数
S = 103.7      # 标的资产当前价格
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# 1. 计算 d1 与 d2 (连续复利)
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 期权价格 (欧式看涨期权 Black-Scholes 公式)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 3. Delta = N(d1)
call_delta = norm.cdf(d1)

# 4. Vega = S * sqrt(T) * n(d1)   (n(d1) 是标准正态密度函数)
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 5. 填充 result 字典，严格按要求的键名
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以便课堂查看 (同时确认数值)
print("计算结果:")
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print(f"看涨期权价格 = {call_price:.6f}")
print(f"Delta = {call_delta:.6f}")
print(f"Vega = {call_vega:.6f}")
print("\nresult 字典内容:", result)

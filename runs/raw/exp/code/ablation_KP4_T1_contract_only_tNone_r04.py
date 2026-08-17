import numpy as np
from scipy.stats import norm

# 参数设置
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率（年化）
r = 0.043      # 无风险利率（年化）
T = 0.58       # 剩余期限（年）

# 计算d1和d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算期权价格 (Black-Scholes公式)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算delta
call_delta = norm.cdf(d1)

# 计算vega (vega = S * sqrt(T) * n(d1)，其中n(d1)是标准正态分布的概率密度函数)
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 将结果存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果
print("欧式看涨期权计算结果:")
print(f"期权价格: {call_price:.4f}")
print(f"Delta: {call_delta:.4f}")
print(f"Vega: {call_vega:.4f}")

# 验证输出契约
print("\n结果字典:")
print(result)

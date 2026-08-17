import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（年化）
r = 0.043          # 无风险利率（年化）
T = 0.58           # 剩余到期时间（年）
q = 0.0            # 股息率（不分红）

# 1. 计算 d1 和 d2
d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格和 delta
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)

# 3. 计算 vega
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T) * 0.01  # 以 1% 波动率变化为单位

# 4. 填充 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（可选，用于调试）
print(result)

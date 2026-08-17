import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（27.6% 年化）
r = 0.043          # 无风险利率（4.3% 连续复利）
T = 0.58           # 剩余期限（年）

# 1. 计算 d1 与 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. vega（每单位波动率变化，即 dC/dσ）
call_vega = S * norm.pdf(d1) * np.sqrt(T)   # 注意：nor.pdf 是标准正态密度

# 4. 填充 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果（精确到6位小数，方便课堂展示）
print(f"期权价格: {result['call_price']:.6f}")
print(f"Delta:     {result['call_delta']:.6f}")
print(f"Vega:      {result['call_vega']:.6f}")

import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
sigma = 0.276      # 年化隐含波动率
r = 0.043          # 无风险利率（年化）
T = 0.58           # 剩余期限（年）

# 1. 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格和 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. 计算 vega（注意：vega 的单位是每 1% 波动率变化对应的价格变化）
call_vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # 乘以 0.01 将单位转换为每 1% 波动率变化

# 4. 填充 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（可选，用于验证）
print(result)

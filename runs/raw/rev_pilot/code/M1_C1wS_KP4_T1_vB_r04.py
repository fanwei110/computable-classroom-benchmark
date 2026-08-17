import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7      # 标的资产价格
K = 97.5       # 行权价格
sigma = 0.276  # 波动率
r = 0.043      # 无风险利率
T = 0.58       # 剩余期限（年）

# 1. 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格和 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. 计算 vega
call_vega = S * norm.pdf(d1) * np.sqrt(T) * 0.01  # 乘以0.01将vega转换为每1%波动率变化的价格变化

# 4. 填充 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（可选，用于验证）
print(result)

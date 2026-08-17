import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 年化波动率（27.6%）
r = 0.043      # 无风险利率（4.3%，连续复利）
T = 0.58       # 剩余期限（年）

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算 delta (N(d1))
call_delta = norm.cdf(d1)

# 计算 vega (每单位波动率变化)
call_vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # 乘以0.01将vega转换为每1%波动率变化的值（题目要求小数表示）

# 由于题目要求vega按每单位波动率（即100%变化）报价，因此不需要乘以0.01
# 修正：题目要求vega按每单位波动率（即1.0变化）报价，因此直接使用公式
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 存储结果
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（可选，用于验证）
print(result)

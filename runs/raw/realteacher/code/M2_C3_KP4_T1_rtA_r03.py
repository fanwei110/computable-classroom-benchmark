import math
import numpy as np

# 输入参数
S0 = 103.7           # 标的现价
K = 97.5             # 行权价
sigma = 0.276        # 隐含波动率
R = 0.043            # 年复利无风险利率（债券收益率报价）
T = 0.58             # 到期年限（按252个交易日为一年计算）

# 将年复利转换为连续复利
r = math.log(1 + R)  # 连续复利无风险利率

# 计算 d1 和 d2
d1 = (math.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 标准正态分布的累积分布函数和概率密度函数
def norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def norm_pdf(x):
    return math.exp(-0.5 * x ** 2) / math.sqrt(2.0 * math.pi)

# 期权价格
call_price = S0 * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

# Delta
call_delta = norm_cdf(d1)

# Vega（标准BS公式中的 Vega = S0 * N'(d1) * sqrt(T)）
call_vega = S0 * norm_pdf(d1) * math.sqrt(T)

# 输出契约
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

result

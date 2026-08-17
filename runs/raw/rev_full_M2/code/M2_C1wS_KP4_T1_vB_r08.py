import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7        # 标的资产价格
K = 97.5         # 行权价
sigma = 0.276    # 波动率（年化）
r = 0.043        # 无风险利率（年化）
T = 0.58         # 剩余到期时间（年）

# 步骤1: 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 步骤2: 计算欧式看涨期权价格与 Delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 步骤3: 计算 Vega（标准 Black-Scholes 闭式解，对波动率 σ 的偏导数）
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 步骤4: 填充结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印输出，便于课堂投屏查看
print(result)

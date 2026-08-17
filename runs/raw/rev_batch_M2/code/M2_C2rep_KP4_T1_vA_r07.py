import numpy as np
from scipy.stats import norm

# ------------------------------
# 给定参数
# ------------------------------
S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 年化隐含波动率
r = 0.043        # 年化无风险利率
T = 0.58         # 剩余期限（年）

# ------------------------------
# 1. 计算 d1 与 d2
# ------------------------------
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ------------------------------
# 2. 计算期权价格与 delta
# ------------------------------
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# ------------------------------
# 3. 计算 vega（波动率每变动 1 单位 对应的期权价格变化）
#    若需换算为波动率每变动 1%（0.01）的情况，可自行除以 100
# ------------------------------
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# ------------------------------
# 4. 填充结果
# ------------------------------
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print(result)

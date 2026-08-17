import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7         # 股票现价
K = 97.5          # 行权价
sigma = 0.276     # 隐含波动率（年化，小数）
r = 0.043         # 无风险利率（连续复利，小数）
T = 0.58          # 剩余期限（年）
q = 0.0           # 股息率（不分红）

# 1. 计算 d1 和 d2
d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. vega（每单位波动率，即 dC/dσ）
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# 4. 填充结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出（供教师投屏检验）
print(result)

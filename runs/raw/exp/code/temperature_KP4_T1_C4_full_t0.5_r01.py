import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的价格
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（小数）
r = 0.043          # 无风险利率（小数）
T = 0.58           # 剩余期限（年）

# 步骤1：计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 步骤2：计算期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 步骤3：计算 vega（每单位波动率）
call_vega = S * norm.pdf(d1) * np.sqrt(T)   # dC/dσ，单位为 元/波动率变化1（小数）

# 步骤4：填充 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果（教师投屏时可见）
print("期权价格:", round(result['call_price'], 4))
print("Delta:", round(result['call_delta'], 4))
print("Vega:", round(result['call_vega'], 4))

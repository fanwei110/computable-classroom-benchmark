import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限（年）

# 步骤1：计算 d1 与 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 步骤2：计算期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 步骤3：计算 vega（每单位波动率的变化）
# vega = S * n(d1) * sqrt(T)  其中 n(d1) 是标准正态密度函数
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 步骤4：将结果存入字典
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

# 输出结果
print("计算过程：")
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print(f"N(d1) = {norm.cdf(d1):.6f}")
print(f"N(d2) = {norm.cdf(d2):.6f}")
print(f"n(d1) = {norm.pdf(d1):.6f}")
print()
print("最终结果：")
print(result)

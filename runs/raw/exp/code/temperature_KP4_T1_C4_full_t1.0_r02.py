import numpy as np
from scipy.stats import norm

# 给定参数
S = 103.7      # 标的资产现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# 1. 计算 d1 与 d2 (连续复利)
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 期权价格与 delta
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. vega (每单位波动率)
call_vega = S * norm.pdf(d1) * np.sqrt(T)   # dC/dσ

# 4. 输出结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 显示结果 (教师投屏可见)
print("计算结果：")
print(f"期权价格 (call_price) = {result['call_price']:.6f}")
print(f"Delta (call_delta)     = {result['call_delta']:.6f}")
print(f"Vega (call_vega)       = {result['call_vega']:.6f}")

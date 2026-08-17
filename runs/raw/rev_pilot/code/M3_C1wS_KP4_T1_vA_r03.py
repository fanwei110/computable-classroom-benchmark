import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
S = 103.7       # 标的现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余到期时间 (年)
q = 0.0         # 股息率 (题目指明不分红)

# ==================== 第1步：计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 第2步：计算期权价格与 delta ====================
# 欧式看涨期权价格 C = S * e^(-qT) * N(d1) - K * e^(-rT) * N(d2)
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 Delta = e^(-qT) * N(d1)
call_delta = np.exp(-q * T) * norm.cdf(d1)

# ==================== 第3步：计算 vega ====================
# Vega = S * e^(-qT) * sqrt(T) * N'(d1)，其中 N'(x) 为标准正态分布的概率密度函数
call_vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)

# ==================== 第4步：填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 课堂投屏展示输出
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"欧式看涨期权价格 = {result['call_price']:.4f}")
print(f"欧式看涨期权 Delta = {result['call_delta']:.4f}")
print(f"欧式看涨期权 Vega  = {result['call_vega']:.4f}")
print("-" * 30)
print("result 字典内容：")
print(result)

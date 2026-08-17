import numpy as np
from scipy.stats import norm

# ==================== 给定参数 ====================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率（年化）
r = 0.043       # 无风险利率（连续复利，年化）
T = 0.58        # 剩余到期时间（年）
q = 0.0         # 股息率（不分红）

# ==================== 1. 计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 2. 计算期权价格与 Delta ====================
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)   # 对于无分红欧式看涨，delta = N(d1)

# ==================== 3. 计算 Vega（价格对波动率的偏导） ====================
call_vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)

# ==================== 4. 填充结果字典 ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 执行时打印结果以供课堂验证
if __name__ == "__main__":
    print(result)

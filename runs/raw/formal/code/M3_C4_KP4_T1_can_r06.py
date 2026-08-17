import numpy as np
from scipy.stats import norm

# ==========================================
# 欧式看涨期权 Black-Scholes 定价与希腊字母计算
# ==========================================

# 1. 设定已知参数（小数表示）
S = 103.7      # 股票现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# 2. 计算 d1 与 d2 (连续复利)
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 3. 计算期权价格与 Delta
# 看涨期权价格 C = S * N(d1) - K * exp(-rT) * N(d2)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 看涨期权 Delta = N(d1)
call_delta = norm.cdf(d1)

# 4. 计算 Vega (按每单位波动率报价 dC/dσ)
# Vega = S * N'(d1) * sqrt(T)，其中 N'(d1) 为标准正态分布的概率密度函数(PDF)
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 5. 按输出契约填充 result 字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 课堂投屏展示结果
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"Call Price: {result['call_price']:.4f}")
print(f"Call Delta: {result['call_delta']:.4f}")
print(f"Call Vega:  {result['call_vega']:.4f}")

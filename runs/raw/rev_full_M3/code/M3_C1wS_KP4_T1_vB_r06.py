import numpy as np
from scipy.stats import norm

# ================== 参数设定 ==================
S = 103.7      # 标的资产价格
K = 97.5       # 行权价
vol = 0.276    # 波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 距到期时间 (年)

# ================== 步骤 1: 计算 d1 与 d2 ==================
d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
d2 = d1 - vol * np.sqrt(T)

# ================== 步骤 2: 计算期权价格与 delta ==================
# 欧式看涨期权不分红 (q=0)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# ================== 步骤 3: 计算 vega ==================
# vega = S * sqrt(T) * N'(d1)，其中 N'(x) 为标准正态分布的概率密度函数
# 注意：此处 vega 为波动率变动 1 个单位（即 100%，或 100个波动率点）时的价格变化量
call_vega = S * np.sqrt(T) * norm.pdf(d1)

# ================== 步骤 4: 填充 result ==================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果，方便课堂投屏展示
print(f"d1 = {d1:.6f}")
print(f"d2 = {d2:.6f}")
print("-" * 30)
print(f"Call Price = {result['call_price']:.4f}")
print(f"Call Delta = {result['call_delta']:.4f}")
print(f"Call Vega  = {result['call_vega']:.4f}")
print("-" * 30)
print("Result Dictionary:")
print(result)

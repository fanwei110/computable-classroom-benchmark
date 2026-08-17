import numpy as np
from scipy.stats import norm

# ====================
// 给定参数
# ====================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (年化 27.6%)
r = 0.043       # 无风险利率 (年化 4.3%)
T = 0.58        # 剩余期限 (年)

# ====================
// 步骤 1：计算 d1 与 d2
# ====================
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ====================
// 步骤 2：计算期权价格与 delta
# ====================
# 欧式看涨期权价格闭式解: C = S * N(d1) - K * exp(-rT) * N(d2)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 Delta: N(d1)
call_delta = norm.cdf(d1)

# ====================
// 步骤 3：计算 vega
# ====================
# Vega 闭式解: S * N'(d1) * sqrt(T)，其中 N' 为标准正态分布的概率密度函数(PDF)
# 注：此处计算的是数学上对波动率sigma的偏导数，若习惯以1%波动率变动报价，通常需除以100
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# ====================
// 步骤 4：填充 result
# ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# ====================
// 课堂输出展示 (投屏友好)
# ====================
print("=" * 45)
print("   Black-Scholes 欧式看涨期权定价与希腊字母")
print("=" * 45)
print(f"【输入参数】")
print(f"  标的现价 (S)    : {S}")
print(f"  行权价   (K)    : {K}")
print(f"  隐含波动率(σ)   : {sigma*100:.1f}%")
print(f"  无风险利率(r)   : {r*100:.1f}%")
print(f"  剩余期限(T)     : {T} 年")
print("-" * 45)
print(f"【中间变量】")
print(f"  d1              : {d1:.6f}")
print(f"  d2              : {d2:.6f}")
print("-" * 45)
print(f"【计算结果】")
print(f"  期权价格: {result['call_price']:.4f}")
print(f"  Delta   : {result['call_delta']:.6f}")
print(f"  Vega    : {result['call_vega']:.6f}  (按1%变动: {result['call_vega']/100:.6f})")
print("=" * 45)

import numpy as np
from scipy.stats import norm

# ==================== 参数设置 ====================
S = 103.7       # 标的现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (27.6%)
r = 0.043       # 无风险利率 (4.3%)
T = 0.58        # 剩余到期时间 (年)
q = 0.0         # 股息率 (题目未指明，假设不分红)

# ==================== 步骤 1: 计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 步骤 2: 计算期权价格与 delta ====================
# 欧式看涨期权闭式解
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 欧式看涨期权 Delta
call_delta = np.exp(-q * T) * norm.cdf(d1)

# ==================== 步骤 3: 计算 vega ====================
# Vega 表示期权价格对波动率的一阶偏导数 (此处为绝对值，即波动率每变动1个单位的价格变化)
# 注：若需波动率变动1%的价格变化，可将其除以100
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# ==================== 步骤 4: 填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# (可选) 打印结果以供课堂投屏验证
if __name__ == "__main__":
    print(f"d1 = {d1:.6f}")
    print(f"d2 = {d2:.6f}")
    print("-" * 30)
    print(f"看涨期权价格 = {result['call_price']:.4f}")
    print(f"看涨期权 Delta = {result['call_delta']:.4f}")
    print(f"看涨期权 Vega  = {result['call_vega']:.4f}")

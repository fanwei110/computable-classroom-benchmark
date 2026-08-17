import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
S = 103.7       # 标的资产现价
K = 97.5        # 行权价
sigma = 0.276   # 年化隐含波动率
r = 0.043       # 无风险利率
T = 0.58        # 剩余期限（年）
q = 0.0         # 股息率（题目指明不分红，故为0）

# ==================== 步骤 1: 计算 d1 与 d2 ====================
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ==================== 步骤 2: 计算期权价格与 delta ====================
# 标准正态分布的累积概率与概率密度
N_d1 = norm.cdf(d1)
N_d2 = norm.cdf(d2)

# 欧式看涨期权价格 (Black-Scholes 闭式解)
call_price = S * np.exp(-q * T) * N_d1 - K * np.exp(-r * T) * N_d2

# 欧式看涨期权 Delta
call_delta = np.exp(-q * T) * N_d1

# ==================== 步骤 3: 计算 vega ====================
n_d1 = norm.pdf(d1)

# Vega (价格对波动率的一阶导数)
call_vega = S * np.exp(-q * T) * np.sqrt(T) * n_d1

# ==================== 步骤 4: 填充 result ====================
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 以下为控制台输出验证（教师投屏时可直接观察中间变量与最终结果）
if __name__ == '__main__':
    print(f"d1 = {d1:.6f}")
    print(f"d2 = {d2:.6f}")
    print("-" * 30)
    print(f"Call Price = {result['call_price']:.4f}")
    print(f"Call Delta = {result['call_delta']:.4f}")
    print(f"Call Vega  = {result['call_vega']:.4f}")

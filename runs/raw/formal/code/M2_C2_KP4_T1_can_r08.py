import numpy as np
from scipy.stats import norm

# ========== 给定参数 ==========
S = 103.7          # 股票现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（年化）
r = 0.043          # 无风险利率（年化）
T = 0.58           # 剩余期限（年）

# ========== 1. 计算 d1 与 d2 ==========
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ========== 2. 计算期权价格与 delta ==========
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# ========== 3. 计算 vega ==========
# vega 通常定义为隐含波动率每变动 1 个百分点（0.01）时期权价格的变化量
# 公式：vega = S * sqrt(T) * N'(d1) * 0.01
call_vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01

# ========== 4. 填充 result ==========
result = {
    'call_price': round(call_price, 6),   # 保留6位小数，便于复现与检查
    'call_delta': round(call_delta, 6),
    'call_vega': round(call_vega, 6)
}

# 输出结果（教师投屏时直接显示）
if __name__ == "__main__":
    print("欧式看涨期权 Black-Scholes 计算")
    print(f"S = {S}, K = {K}, σ = {sigma}, r = {r}, T = {T}\n")
    print(f"d1 = {d1:.6f}")
    print(f"d2 = {d2:.6f}")
    print(f"看涨期权价格 = {result['call_price']:.6f}")
    print(f"Delta = {result['call_delta']:.6f}")
    print(f"Vega = {result['call_vega']:.6f}  (波动率每+1%时的价格变动)")
    print("\nresult 字典：", result)

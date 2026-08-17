import numpy as np
from scipy.stats import norm

# === 输入参数 ===
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率 (27.6%)
r = 0.043          # 无风险利率 (4.3%)
T = 0.58           # 剩余到期时间（年）
q = 0.0            # 不分红，股息率设为0

# === 步骤1: 计算 d1 与 d2 ===
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# === 步骤2: 计算期权价格与 Delta ===
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)   # 看涨期权 Delta

# === 步骤3: 计算 Vega ===
# Vega 定义为隐含波动率每变动 1 个百分点（0.01）时期权价格的变化。
# 数学上 BS Vega = S * exp(-q*T) * N'(d1) * sqrt(T)，这里乘以 0.01 以匹配 1% 的变动。
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T) * 0.01

# === 步骤4: 填入结果 ===
result = {
    'call_price': round(call_price, 6),
    'call_delta': round(call_delta, 6),
    'call_vega': round(call_vega, 6)
}

# 输出结果供投屏展示
if __name__ == "__main__":
    print("Black-Scholes 欧式看涨期权定价结果")
    print(f"标的现价 S = {S}")
    print(f"行权价 K = {K}")
    print(f"隐含波动率 σ = {sigma*100:.1f}%")
    print(f"无风险利率 r = {r*100:.2f}%")
    print(f"剩余期限 T = {T} 年")
    print("-" * 40)
    print(f"d1 = {d1:.6f}")
    print(f"d2 = {d2:.6f}")
    print(f"期权价格 (call_price): {result['call_price']}")
    print(f"Delta   (call_delta): {result['call_delta']}")
    print(f"Vega    (call_vega) : {result['call_vega']} (每1%波动率变动)")

    # 最终 result 字典供教师使用
    print("\n>>> result =", result)

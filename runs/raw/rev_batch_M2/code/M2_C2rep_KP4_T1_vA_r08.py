import numpy as np
from scipy.stats import norm

# ---------- 给定参数 ----------
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（年化）
r = 0.043          # 无风险利率（年化）
T = 0.58           # 剩余期限（年）
q = 0.0            # 不分红股票，股息率设为0

# ---------- 1. 计算 d1 与 d2 ----------
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ---------- 2. 计算期权价格与 delta ----------
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)        # 分红为0时简化为 norm.cdf(d1)

# ---------- 3. 计算 vega ----------
# 闭式解 vega = S * exp(-q*T) * sqrt(T) * N'(d1)
# 注意：此处 vega 是价格对波动率（小数）的偏导数，即波动率变化1（100%）时的价格变化。
# 若需转换为波动率每变化1个百分点（0.01）的敏感度，需额外乘以0.01。
call_vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)

# ---------- 4. 填充结果字典 ----------
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

print("计算结果：")
print(f"d1 = {d1:.6f}, d2 = {d2:.6f}")
print(f"看涨期权价格 = {call_price:.4f}")
print(f"Delta = {call_delta:.4f}")
print(f"Vega = {call_vega:.4f} (对波动率小数的偏导数)")
print("\nresult 字典内容：")
print(result)

import numpy as np
from scipy.stats import norm

# ---------- 给定参数 ----------
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（27.6%）
r = 0.043          # 无风险利率（4.3%）
T = 0.58           # 剩余期限（年）
q = 0.0            # 不分红

# ---------- 1. 计算 d1 与 d2 ----------
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ---------- 2. 价格与 delta ----------
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)   # 不分红时即 norm.cdf(d1)

# ---------- 3. vega（对波动率的一阶偏导） ----------
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# ---------- 4. 填充结果字典 ----------
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

if __name__ == '__main__':
    for key, val in result.items():
        print(f"{key}: {val:.6f}")

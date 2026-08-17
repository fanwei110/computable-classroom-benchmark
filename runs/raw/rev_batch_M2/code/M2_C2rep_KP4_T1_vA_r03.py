import numpy as np
from scipy.stats import norm

# ----- 给定的参数 -----
S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 年化隐含波动率
r = 0.043        # 年化无风险利率
T = 0.58         # 剩余期限（年）

# ----- 1. 计算 d1 和 d2 -----
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# ----- 2. 计算看涨期权价格与 delta -----
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# ----- 3. 计算 vega （原始数学导数，对 sigma 的偏导）-----
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# ----- 4. 按要求组织结果 -----
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以供投屏展示
if __name__ == '__main__':
    print("Black-Scholes 欧式看涨期权计算结果：")
    print(f"d1 = {d1:.6f}")
    print(f"d2 = {d2:.6f}")
    print(f"看涨期权价格 = {call_price:.4f}")
    print(f"Delta       = {call_delta:.6f}")
    print(f"Vega        = {call_vega:.6f}")
    print("\n结果字典：")
    print(result)

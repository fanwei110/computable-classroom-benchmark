import numpy as np
from scipy.stats import norm

# 市场参数
S0 = 103.7       # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 年化波动率
r = 0.043        # 无风险利率
T = 0.58         # 剩余期限（年）

# 1. 计算 d1 与 d2
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格与 Delta
call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)

# 3. 计算 Vega (dC/dσ)
call_vega = S0 * norm.pdf(d1) * np.sqrt(T)

# 4. 填充结果
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 可选：打印结果以供核对
if __name__ == '__main__':
    for key, value in result.items():
        print(f"{key}: {value:.6f}")

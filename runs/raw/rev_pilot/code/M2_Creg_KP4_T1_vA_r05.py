import numpy as np
from scipy.stats import norm

# 给定的期权参数
S0 = 103.7        # 标的现价
K = 97.5          # 行权价
T = 0.58          # 剩余期限（年）
r = 0.043         # 无风险利率（年化）
sigma = 0.276     # 隐含波动率（年化）

# Black-Scholes 公式计算 d1 和 d2
d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 看涨期权价格
call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = norm.cdf(d1)

# Vega：波动率每增加1%（即0.01）时，期权价格的变动
# 传统 Black-Scholes vega（对 sigma 的偏导数）乘以 0.01
call_vega = S0 * norm.pdf(d1) * np.sqrt(T) * 0.01

# 将所有结果存入要求输出的字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出结果，便于查看
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.6f}")

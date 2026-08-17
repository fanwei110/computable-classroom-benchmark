import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7           # 标的现价
K = 97.5            # 行权价
sigma = 0.276       # 隐含波动率（小数）
r_annual = 0.043    # 年复利无风险利率（小数）
T = 0.58            # 剩余年限

# 将年复利转换为连续复利
r = np.log(1 + r_annual)

# Black-Scholes 公式
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = norm.cdf(d1)
call_vega  = S * norm.pdf(d1) * np.sqrt(T)   # 对σ（小数形式）的偏导数

result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

result

import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率
r = 0.043          # 无风险利率
T = 0.58           # 剩余到期时间
q = 0.0            # 不分红

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 欧式看涨期权价格
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = np.exp(-q * T) * norm.cdf(d1)

# Vega（注意：基于σ变动1，即100%波动率变化的敏感度，通常除以100表示1%波动率变化）
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# 输出结果字典
result = {
    'call_price': round(call_price, 6),
    'call_delta': round(call_delta, 6),
    'call_vega': round(call_vega, 6)
}

# 打印结果以便验证
print(result)

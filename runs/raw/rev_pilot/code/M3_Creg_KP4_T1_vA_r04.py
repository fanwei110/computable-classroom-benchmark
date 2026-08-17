import numpy as np
from scipy.stats import norm

# 已知参数
S = 103.7       # 现价
K = 97.5        # 行权价
sigma = 0.276   # 隐含波动率 (年化 27.6%)
r = 0.043       # 无风险利率 (年化 4.3%)
T = 0.58        # 剩余期限 (年)

# 计算 Black-Scholes 模型中的 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 计算欧式看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# 计算看涨期权 Delta
call_delta = norm.cdf(d1)

# 计算看涨期权 Vega (对波动率的一阶偏导数 dC/d_sigma)
# 注：金融报价惯例中，Vega通常按波动率每变动1%(即0.01)来报价，此时需除以100。
# 此处按数学偏导数的绝对值输出，若需1%变动报价，可除以100。
call_vega = S * norm.pdf(d1) * np.sqrt(T)

# 按输出契约存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以供验证
print(result)

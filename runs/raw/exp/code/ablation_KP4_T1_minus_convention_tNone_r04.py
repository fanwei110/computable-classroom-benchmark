import numpy as np
from scipy.stats import norm

# 参数
S = 103.7        # 当前股价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率（年化）
r = 0.043        # 无风险利率（年化连续复利）
T = 0.58         # 剩余期限（年）

# 计算 d1 与 d2 （连续复利假设已隐含在公式中）
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 期权价格 (Black-Scholes 欧式看涨)
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta (看涨)
call_delta = norm.cdf(d1)

# Vega (每单位波动率变化带来的价格变化，以小数表示)
call_vega = S * norm.pdf(d1) * np.sqrt(T)   # dC/dσ

# 构造结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 输出（课堂展示用，数值保留足够精度）
print("期权价格: {:.6f}".format(result['call_price']))
print("Delta: {:.6f}".format(result['call_delta']))
print("Vega: {:.6f}".format(result['call_vega']))

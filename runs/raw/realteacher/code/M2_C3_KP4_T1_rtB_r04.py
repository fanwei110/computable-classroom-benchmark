import numpy as np
from scipy.stats import norm

# 已知参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 隐含波动率（小数）
r_ann = 0.043      # 年复利无风险利率（小数）
T = 0.58           # 剩余年限
q = 0.0            # 不分红

# 将年复利利率转换为连续复利
r = np.log(1 + r_ann)

# 计算 d1, d2
sqrt_T = np.sqrt(T)
d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt_T)
d2 = d1 - sigma * sqrt_T

# 期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta
call_delta = norm.cdf(d1)

# Vega（波动率每变动1单位（即100个百分点）对应的期权价格变动）
call_vega = S * norm.pdf(d1) * sqrt_T

# 按要求存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果以验证
print(result)

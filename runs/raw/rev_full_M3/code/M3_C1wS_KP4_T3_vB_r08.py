import numpy as np
from scipy.stats import norm

def calculate_bs_vega(S, K, T, r, sigma):
    """
    计算欧式期权的 Black-Scholes Vega (对看涨和看跌期权相同)
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    return vega

# 题目给定的参数
S = 103.7      # 标的资产价格
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 到期时间 (年)

# 计算当前波动率下的 Vega
vega = calculate_bs_vega(S, K, T, r, sigma)

# IV 涨1个点，即隐含波动率增加 1 个百分点 (1% = 0.01)
delta_sigma = 0.01

# 利用 Vega 推算期权价格对这 1 个百分点波动率变化的响应
price_change = vega * delta_sigma

# 将结果存入符合契约的字典中
result = {'price_change': price_change}

# 教师投屏展示时可直接运行查看结果
print(f"推算的期权价格变化: {result['price_change']:.4f}")

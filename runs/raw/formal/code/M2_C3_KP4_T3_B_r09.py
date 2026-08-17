import numpy as np

S = 103.7      # 标的资产价格
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率
r = 0.043      # 连续复利无风险利率
T = 0.58       # 剩余期限（年）

# 计算 d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
# 计算 vega（波动率变动1单位，即100%时的期权价格变动）
vega = S * np.exp(-0.5 * d1**2) / np.sqrt(2 * np.pi) * np.sqrt(T)
# IV上涨1个点（0.01）对应的价格变动
price_change = vega * 0.01

result = {'price_change': round(price_change, 4)}
print(result)

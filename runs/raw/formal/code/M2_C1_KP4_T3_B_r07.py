import math

# 给定参数
S = 103.7      # 标的价格
K = 97.5       # 行权价
sigma = 0.276  # 初始隐含波动率
r = 0.043      # 无风险利率
T = 0.58       # 期限（年）
delta_sigma = 0.01  # IV 上涨1个百分点

# 计算 d1
d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))

# 标准正态分布概率密度函数 N'(d1)
pdf_d1 = math.exp(-d1**2 / 2) / math.sqrt(2 * math.pi)

# Vega（波动率变化1（即100%）时期权价格的变化）
vega = S * pdf_d1 * math.sqrt(T)

# IV涨1个点（0.01）对应的价格变化
price_change = vega * delta_sigma

result = {
    'price_change': round(price_change, 6)  # 保留6位小数
}

result

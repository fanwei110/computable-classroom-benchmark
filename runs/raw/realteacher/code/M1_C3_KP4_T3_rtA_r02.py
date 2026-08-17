import numpy as np
from scipy.stats import norm

def calculate_vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * norm.pdf(d1)
    return vega

# 假设期权参数（示例值，需替换为实际值）
S = 100       # 标的资产价格
K = 100       # 行权价
T = 0.5       # 到期时间（年）
r = 0.05      # 无风险利率（连续复利）
sigma = 0.2   # 隐含波动率

# 计算Vega
vega = calculate_vega(S, K, T, r, sigma)

# 隐波上涨1个点（0.01）时的价格变化
price_change = vega * 0.01

# 存入结果字典
result = {
    'price_change': price_change
}

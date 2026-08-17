import numpy as np
from scipy.stats import norm

def calculate_vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * norm.pdf(d1) * 0.01  # Vega通常以1%波动率变化为单位，这里乘以0.01转换为1个点（0.01）的变化
    return vega

# 示例参数（假设值，实际应替换为题目中的具体值）
S = 100      # 标的价格
K = 100      # 行权价
T = 0.5      # 到期时间（年）
r = 0.05     # 无风险利率（连续复利）
sigma = 0.2  # 隐含波动率

vega = calculate_vega(S, K, T, r, sigma)
price_change = vega * 1  # 隐波变化1个点（0.01）时的价格变化

result = {
    'price_change': price_change
}

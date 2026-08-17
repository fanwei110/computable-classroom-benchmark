import numpy as np

# 示例参数（若实际期权参数不同，请替换）
S = 100.0      # 标的现价
K = 100.0      # 行权价
r = 0.05       # 无风险利率（连续复利）
T = 1.0        # 到期时间（年）
sigma = 0.20   # 当前隐波
d_sigma = 0.01 # 隐波变化（1个点）

d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
vega = S * np.exp(-d1**2/2) / np.sqrt(2*np.pi) * np.sqrt(T)  # 波动率变动1单位的价格变化
price_change = vega * d_sigma

result = {'price_change': round(price_change, 6)}
print(result)

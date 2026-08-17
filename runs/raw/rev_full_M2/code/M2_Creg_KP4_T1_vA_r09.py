import numpy as np
from scipy.stats import norm

# 给定的期权参数
S = 103.7          # 标的现价
K = 97.5           # 行权价
sigma = 0.276      # 年化隐含波动率（小数形式）
r = 0.043          # 年化无风险利率
T = 0.58           # 剩余期限（年）

# 计算 d1 和 d2
d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 欧式看涨期权价格
call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Delta：期权价格对标的资产价格的偏导数
call_delta = norm.cdf(d1)

# Vega：波动率每变动 1%（绝对值 0.01）期权价格的变化
call_vega = S * norm.pdf(d1) * np.sqrt(T) * 0.01

# 输出结果存入字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 用于验证的可选打印（不会影响 result 字典）
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.6f}")

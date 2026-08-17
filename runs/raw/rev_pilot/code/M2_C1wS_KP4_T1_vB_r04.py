import numpy as np
from scipy.stats import norm

# 输入参数
S = 103.7        # 标的资产价格
K = 97.5         # 行权价
sigma = 0.276    # 波动率
r = 0.043        # 无风险利率
T = 0.58         # 剩余期限（年）
q = 0.0          # 不分红，股息率设为0

# 1. 计算 d1 与 d2
d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)

# 2. 计算期权价格与 delta
call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
call_delta = np.exp(-q * T) * norm.cdf(d1)

# 3. 计算 vega（期权价格对波动率的一阶偏导）
call_vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

# 4. 填充结果字典
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

# 打印结果供课堂投屏查看（保留足够小数位以保证可复现）
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.8f}")

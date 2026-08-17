import numpy as np
from scipy.stats import norm

# 期权参数
S = 103.7          # 标的资产现价
K = 97.5           # 行权价
r = 0.043          # 无风险利率
T = 0.58           # 剩余到期时间（年）
sigma_initial = 0.276  # 初始隐含波动率 (27.6%)
sigma_new = 0.286      # 上升1个百分点后的隐含波动率 (28.6%)

def black_scholes_call_price(S, K, r, T, sigma):
    """
    使用 Black-Scholes 模型计算无股息欧式看涨期权的价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# 计算波动率变化前的期权价格
price_initial = black_scholes_call_price(S, K, r, T, sigma_initial)

# 计算波动率上升1个百分点后的期权价格
price_new = black_scholes_call_price(S, K, r, T, sigma_new)

# 计算期权价格的变化量
price_change = price_new - price_initial

# 按照输出契约存入字典
result = {'price_change': price_change}

# (可选) 打印结果以供验证
if __name__ == "__main__":
    print(f"初始期权价格: {price_initial:.4f}")
    print(f"新期权价格: {price_new:.4f}")
    print(f"价格变化量: {price_change:.4f}")
    print(f"result字典: {result}")

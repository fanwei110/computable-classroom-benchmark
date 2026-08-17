import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """欧式看涨期权 Black-Scholes 定价"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price, d1, d2

def vega(S, K, T, r, sigma):
    """Vega：波动率变动1单位（100%）对应的价格变动"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)

# 给定的期权参数
S = 103.7          # 标的资产价格
K = 97.5           # 行权价
T = 0.58           # 剩余期限（年）
r = 0.043          # 无风险利率
sigma0 = 0.276     # 当前波动率 (27.6%)
delta_sigma = 0.01 # IV 上涨 1 个百分点 (即 1%)

# 方法1：直接计算两个波动率下的期权价格之差
price0, _, _ = black_scholes_call(S, K, T, r, sigma0)
price1, _, _ = black_scholes_call(S, K, T, r, sigma0 + delta_sigma)
price_change = price1 - price0

# 方法2（验证用，不改变最终输出）：使用 Vega 闭式解乘以 0.01
vega_value = vega(S, K, T, r, sigma0)
price_change_vega = vega_value * delta_sigma

# 输出要求的结果
result = {'price_change': price_change}

if __name__ == '__main__':
    print("期权价格变化 (σ 从 27.6% 升至 28.6%):")
    print(f"精确价格差:          {price_change:.6f}")
    print(f"Vega 近似:           {price_change_vega:.6f}")
    print("\n结果字典:")
    print(result)

from scipy.stats import norm
import math

def black_scholes_call(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return call_price

# 输入参数
S = 103.7  # 标的价格
K = 97.5   # 行权价
T = 0.58   # 剩余时间（年）
r = 0.043  # 无风险利率
sigma_initial = 0.276  # 初始波动率
sigma_new = 0.286      # 波动率增加1个百分点

# 计算初始期权价格
price_initial = black_scholes_call(S, K, T, r, sigma_initial)

# 计算波动率增加后的期权价格
price_new = black_scholes_call(S, K, T, r, sigma_new)

# 计算价格变化
price_change = price_new - price_initial

# 存入结果字典
result = {
    'price_change': price_change
}

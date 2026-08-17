import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算欧式看涨期权的 Black-Scholes 价格
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 给定参数
spot_price = 103.7       # 现价
strike_price = 97.5      # 行权价
volatility = 0.276       # 初始波动率 (27.6%)
risk_free_rate = 0.043   # 无风险利率 (4.3%)
time_to_maturity = 0.58  # 剩余期限 (年)

# 计算初始期权价格
initial_call_price = black_scholes_call(spot_price, strike_price, time_to_maturity, risk_free_rate, volatility)

# 波动率上升一个百分点 (即绝对值增加 0.01)
new_volatility = volatility + 0.01

# 计算波动率上升后的新期权价格
new_call_price = black_scholes_call(spot_price, strike_price, time_to_maturity, risk_free_rate, new_volatility)

# 计算期权价格的变化量
price_change = new_call_price - initial_call_price

# 按照输出契约存入字典
result = {'price_change': price_change}

# 打印结果以供验证
print(result)

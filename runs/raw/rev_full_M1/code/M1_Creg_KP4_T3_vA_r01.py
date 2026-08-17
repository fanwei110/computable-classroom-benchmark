import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    计算 Black-Scholes 看涨期权价格
    S: 标的资产现价
    K: 行权价
    T: 剩余期限（年）
    r: 无风险利率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

# 输入参数
current_price = 103.7
strike_price = 97.5
time_to_maturity = 0.58
risk_free_rate = 0.043
initial_volatility = 0.276
volatility_increase = 0.01  # 1% 的增加

# 计算初始期权价格
initial_option_price = black_scholes_call(
    S=current_price,
    K=strike_price,
    T=time_to_maturity,
    r=risk_free_rate,
    sigma=initial_volatility
)

# 计算波动率增加后的期权价格
new_volatility = initial_volatility + volatility_increase
new_option_price = black_scholes_call(
    S=current_price,
    K=strike_price,
    T=time_to_maturity,
    r=risk_free_rate,
    sigma=new_volatility
)

# 计算价格变化
price_change = new_option_price - initial_option_price

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，根据需要）
print(result)

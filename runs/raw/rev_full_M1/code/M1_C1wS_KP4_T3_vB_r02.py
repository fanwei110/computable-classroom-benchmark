import numpy as np
from scipy.stats import norm

# 输入参数
option_bid = 103.7  # 期权买价
option_ask = 97.5   # 期权卖价
iv = 0.276         # 隐含波动率 (27.6%)
risk_free_rate = 0.043  # 无风险利率 (4.3%)
time_to_maturity = 0.58  # 距离到期时间 (0.58年)

# 从买卖价中推断期权中间价作为当前价格
option_price = (option_bid + option_ask) / 2

# 反推行权价（假设期权为平价期权，即 S ≈ K）
# 这里使用 Black-Scholes 反推 K，但实际应用中 K 应已知
# 为简化，假设 S = K（平价期权），因为题目未给出 S 或 K
S = option_price  # 假设标的资产价格 S ≈ K（平价期权近似）
K = S             # 行权价 K ≈ S

# Black-Scholes 公式计算期权价格
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# 计算 Vega（波动率变化对期权价格的影响）
def vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * np.sqrt(T) * norm.pdf(d1)

# 计算当前 Vega
current_vega = vega(S, K, time_to_maturity, risk_free_rate, iv)

# IV 上涨 1 个百分点（0.01）时的价格变化
iv_change = 0.01
price_change = current_vega * iv_change

# 存储结果
result = {
    'price_change': price_change
}

# 输出结果（可选，用于调试）
print(result)

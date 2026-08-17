import math

S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率
r = 0.043        # 无风险利率（连续复利）
T = 0.58         # 剩余期限（年）
q = 0.0          # 不分红

# 计算 d1, d2
d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 标准正态分布的概率密度函数和累积分布函数
def norm_pdf(x):
    return math.exp(-x**2 / 2) / math.sqrt(2 * math.pi)

def norm_cdf(x):
    # 使用高精度近似公式 (Abramowitz and Stegun)
    p = 0.2316419
    b1 = 0.319381530
    b2 = -0.356563782
    b3 = 1.781477937
    b4 = -1.821255978
    b5 = 1.330274429
    if x >= 0:
        t = 1.0 / (1.0 + p * x)
        poly = b1*t + b2*t**2 + b3*t**3 + b4*t**4 + b5*t**5
        return 1.0 - norm_pdf(x) * poly
    else:
        return 1.0 - norm_cdf(-x)

# 期权价格、Delta、Vega
call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
call_delta = norm_cdf(d1)
call_vega = S * norm_pdf(d1) * math.sqrt(T)  # 波动率每变动1单位（100%）的期权价格变化

result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

result

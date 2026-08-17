import math

# 参数
S = 103.7        # 标的现价
K = 97.5         # 行权价
sigma = 0.276    # 隐含波动率
r = 0.043        # 无风险利率
T = 0.58         # 到期时间

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 标准正态分布的概率密度函数和累积分布函数
# 使用 math.erf 计算累积分布
def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def norm_pdf(x):
    return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x**2)

# 期权价格、Delta、Vega
call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
call_delta = norm_cdf(d1)
call_vega = S * norm_pdf(d1) * math.sqrt(T)   # 对波动率(小数形式)的导数

# 存入字典，保留4位小数
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print(result)

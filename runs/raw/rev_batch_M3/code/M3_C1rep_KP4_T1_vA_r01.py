import math

# 已知参数
S = 103.7    # 标的现价
K = 97.5     # 行权价
sigma = 0.276 # 隐含波动率
r = 0.043    # 无风险利率
T = 0.58     # 剩余到期时间(年)
q = 0.0      # 股息率

# 计算d1和d2
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 正态分布累积概率函数和概率密度函数
def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def norm_pdf(x):
    return math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)

# 计算期权价格
call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

# 计算Delta
call_delta = norm_cdf(d1)

# 计算Vega (原始值，即波动率变化1个单位时期权价格的变化；若需波动率变化1%时的Vega，可除以100)
call_vega = S * math.sqrt(T) * norm_pdf(d1)

# 将结果存入字典
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

print(result)

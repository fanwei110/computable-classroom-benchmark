import math

# 输入参数
S = 103.7
K = 97.5
sigma = 0.276
r = 0.043
T = 0.58

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 标准正态累积分布函数近似（使用 math.erf）
def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))
def norm_pdf(x):
    return 1.0 / math.sqrt(2 * math.pi) * math.exp(-0.5 * x * x)

# 期权价格、delta、vega
call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
call_delta = norm_cdf(d1)
call_vega = S * norm_pdf(d1) * math.sqrt(T)  # ∂C/∂σ，其中 σ 使用小数表示

# 按要求存入字典
result = {
    'call_price': round(call_price, 6),
    'call_delta': round(call_delta, 6),
    'call_vega': round(call_vega, 6)
}

# 打印结果（仅用于展示）
print(result)

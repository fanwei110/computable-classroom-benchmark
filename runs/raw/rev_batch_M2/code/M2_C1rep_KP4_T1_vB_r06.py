import math

# 参数
S = 103.7          # 标的资产价格
K = 97.5           # 行权价
sigma = 0.276      # 波动率 (27.6%)
r = 0.043          # 无风险利率
T = 0.58           # 剩余期限（年）

# 计算 d1, d2
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 标准正态分布的累积分布函数 (CDF)
def norm_cdf(x):
    """标准正态累计分布函数"""
    # 使用近似公式
    a1, a2, a3, a4, a5 = 0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429
    k = 1.0 / (1.0 + 0.2316419 * abs(x))
    n_prime = math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    y = 1.0 - n_prime * (a1*k + a2*k**2 + a3*k**3 + a4*k**4 + a5*k**5)
    return y if x >= 0 else 1.0 - y

# 标准正态分布的概率密度函数 (PDF)
def norm_pdf(x):
    return math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)

# 计算价格
call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

# 计算 delta
call_delta = norm_cdf(d1)

# 计算 vega (波动率每变化 1 单位（即 100%）时的价格变化，BSM 偏导数)
call_vega = S * norm_pdf(d1) * math.sqrt(T)

# 存储结果
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)
}

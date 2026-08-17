import math

# 已知参数
S = 103.7      # 标的资产价格
K = 97.5       # 行权价
vol = 0.276    # 波动率 (27.6%)
r = 0.043      # 无风险利率 (4.3%)
T = 0.58       # 剩余期限 (年)

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * math.sqrt(T))
d2 = d1 - vol * math.sqrt(T)

# 正态分布累积概率函数和概率密度函数的近似计算
def norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def norm_pdf(x):
    return math.exp(-0.5 * x**2) / math.sqrt(2.0 * math.pi)

# 计算 Call Price
call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

# 计算 Delta (欧式不分红看涨期权)
call_delta = norm_cdf(d1)

# 计算 Vega (对波动率的导数，通常按绝对值计，即 vol 变动 1 单位对应的价格变化)
call_vega = S * norm_pdf(d1) * math.sqrt(T)

# 按照契约输出字典
result = {
    'call_price': round(call_price, 4),
    'call_delta': round(call_delta, 4),
    'call_vega': round(call_vega, 4)  # 注：此处为数学定义原始Vega，若交易习惯看1%变动需除以100
}

import math
from scipy.stats import norm

# 输入参数
S = 103.7      # 标的现价
K = 97.5       # 行权价
sigma = 0.276  # 隐含波动率 (小数表示)
r = 0.043      # 无风险利率 (小数表示，连续复利)
T = 0.58       # 剩余期限 (年)
q = 0.0        # 股息率 (不分红)

# 计算 d1 和 d2
d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)

# 计算欧式看涨期权价格
call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# 计算 Delta
call_delta = norm.cdf(d1)

# 计算 Vega (通常按绝对值变动1%即0.01来报价，这里计算的是每1单位波动率变动的绝对敏感度)
# 公式为 S * N'(d1) * sqrt(T)，为了符合常规以1%为单位，可乘以0.01，但按严格定义输出原始值乘0.01更符合业界vega读数习惯
# 通常Vega输出为：变动1个Volatility Point (1%=0.01) 的价格变化，即 S * norm.pdf(d1) * math.sqrt(T) * 0.01
call_vega = S * norm.pdf(d1) * math.sqrt(T) * 0.01

# 封装结果
result = {
    'call_price': call_price,
    'call_delta': call_delta,
    'call_vega': call_vega
}

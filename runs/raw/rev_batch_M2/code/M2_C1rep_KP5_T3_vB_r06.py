import math

# 给定参数
annual_vol = 0.24
position = 2_700_000
confidence = 0.95
trading_days = 252

# 95%置信水平对应的正态分布分位数（单尾）
z_score = 1.6448536269514722

# 日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 一日VaR
var_95_1d = position * z_score * daily_vol

# 结果存入字典
result = {
    'var_95_1d': round(var_95_1d, 2)
}

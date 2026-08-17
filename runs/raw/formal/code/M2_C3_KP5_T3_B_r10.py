import math

# 给定参数
annual_vol = 0.24
position = 2_700_000
confidence = 0.95
trading_days = 252

# 年化波动率转为日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 95% 置信度对应的正态分布分位数
z_95 = 1.6448536269514722  # scipy.stats.norm.ppf(0.95)

# 一日 VaR（损失金额取正）
var_95_1d = position * daily_vol * z_95

result = {'var_95_1d': round(var_95_1d, 2)}

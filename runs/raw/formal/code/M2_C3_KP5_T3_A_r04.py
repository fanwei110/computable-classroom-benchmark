import math
from scipy.stats import norm

# 给定数据
annual_vol = 0.24
position = 2_700_000
trading_days = 252
confidence = 0.95

# 计算单日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 计算标准正态分布的95%分位数
z_score = norm.ppf(confidence)

# 计算一日VaR（损失金额，正数表示损失）
var_95_1d = position * daily_vol * z_score

# 按要求输出字典
result = {'var_95_1d': round(var_95_1d, 2)}

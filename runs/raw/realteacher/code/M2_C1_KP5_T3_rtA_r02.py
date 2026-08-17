import math
from scipy.stats import norm

# 参数
annual_volatility = 0.24
position = 2_700_000  # 270万
confidence_level = 0.95
trading_days = 252

# 计算日波动率
daily_volatility = annual_volatility / math.sqrt(trading_days)

# 95%置信度对应的z分数（单尾）
z_score = norm.ppf(confidence_level)  # 约1.64485

# 一日VaR
var_95_1d = position * daily_volatility * z_score

# 输出字典，保留两位小数
result = {'var_95_1d': round(var_95_1d, 2)}
result

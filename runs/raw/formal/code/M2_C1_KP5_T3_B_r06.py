import numpy as np
from scipy.stats import norm

# 输入参数
position = 2_700_000          # 头寸270万
annual_vol = 0.24             # 年化波动率24%
confidence = 0.95             # 置信水平
trading_days = 252            # 年交易日，通常取252

# 计算一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 计算95%置信度的z值（单尾）
z_score = norm.ppf(confidence)

# 计算VaR
var_95_1d = position * daily_vol * z_score

# 结果保留两位小数
result = {'var_95_1d': round(var_95_1d, 2)}
result

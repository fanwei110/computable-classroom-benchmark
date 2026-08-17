import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24
position = 2700000
confidence = 0.95
days = 252  # 一年交易日

# 计算一日波动率
daily_vol = annual_vol / np.sqrt(days)

# 计算95%置信水平下的z值
z_score = norm.ppf(confidence)

# 计算VaR
var_95_1d = position * daily_vol * z_score

result = {'var_95_1d': round(var_95_1d, 2)}

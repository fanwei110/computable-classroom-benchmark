import numpy as np
from scipy.stats import norm

# 给定数据
annual_vol = 0.24
position = 2_700_000
trading_days = 252
confidence = 0.95

# 一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 95% 置信水平的 z 值
z_95 = norm.ppf(confidence)

# 一日 VaR
var_95_1d = position * z_95 * daily_vol

result = {'var_95_1d': round(var_95_1d, 2)}

import numpy as np

# 已知参数
annual_vol = 0.24
position = 2700000
confidence = 0.95
trading_days = 252

# 计算日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 95% 置信水平对应的 z 值
z_95 = 1.6448536269514722

# 计算一日 VaR
var_95_1d = position * daily_vol * z_95

result = {'var_95_1d': round(var_95_1d, 2)}

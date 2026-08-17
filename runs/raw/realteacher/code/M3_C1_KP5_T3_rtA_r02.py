import math

# 已知参数
annual_vol = 0.24  # 年化波动率 24%
position = 2700000  # 头寸 270万
z_score_95 = 1.645  # 95%置信水平下的Z值
trading_days = 252  # 一般默认一年252个交易日

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 计算 95% 一日 VaR
var_95_1d = position * daily_vol * z_score_95

# 按照输出契约存入字典
result = {'var_95_1d': round(var_95_1d, 2)}

result

import math

# 已知参数
annual_vol = 0.24          # 年化波动率
position = 2700000         # 头寸规模
z_95 = 1.64485362695       # 95%置信水平下的Z分数（正态分布分位数）
trading_days = 252         # 一年交易日天数（金融市场计算VaR的惯例）

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 计算95%一日VaR
var_95_1d = position * z_95 * daily_vol

# 按要求输出契约存入字典
result = {'var_95_1d': round(var_95_1d, 2)}

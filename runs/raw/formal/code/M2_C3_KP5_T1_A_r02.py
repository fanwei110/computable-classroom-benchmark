import math
from scipy.stats import norm

# 给定参数
position = 1850000          # 头寸（元）
annual_vol = 0.218          # 年化波动率
trading_days = 252          # 年交易日数

# 置信水平对应的 z 值（单侧 VaR）
z_95 = norm.ppf(0.95)       # 1.6448536269514722
z_99 = norm.ppf(0.99)       # 2.3263478740408408

# 计算一日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 95% 置信水平的一日 VaR
var_95_1d = position * daily_vol * z_95

# 计算十日波动率（时间平方根法则）
ten_day_vol = annual_vol * math.sqrt(10 / trading_days)

# 99% 置信水平的十日 VaR
var_99_10d = position * ten_day_vol * z_99

# 将结果存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

import math

# 输入参数
position = 1_850_000  # 头寸，单位元
annual_vol = 0.218    # 年化波动率
trading_days = 252    # 年交易日数

# 置信水平对应的 Z 值（标准正态分布单尾分位数）
z_95 = 1.645  # 95%
z_99 = 2.326  # 99%

# 1日波动率
vol_1d = annual_vol / math.sqrt(trading_days)
# 10日波动率
vol_10d = annual_vol * math.sqrt(10 / trading_days)

# 参数法 VaR 计算（假设均值为0）
var_95_1d = position * z_95 * vol_1d
var_99_10d = position * z_99 * vol_10d

# 结果存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

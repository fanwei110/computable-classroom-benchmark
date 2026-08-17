import math

# 已知参数
position = 1850000  # 头寸185万元
annual_vol = 0.218  # 年化波动率21.8%
trading_days = 252  # 假设一年252个交易日

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 正态分布分位数 (参数法常用近似值)
z_95 = 1.645
z_99 = 2.326

# 计算 95%置信水平的一日VaR
var_95_1d = position * z_95 * daily_vol * math.sqrt(1)

# 计算 99%置信水平的十日VaR
var_99_10d = position * z_99 * daily_vol * math.sqrt(10)

# 按照输出契约存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

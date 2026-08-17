import math

# 参数
position = 1_850_000          # 头寸
annual_vol = 0.218           # 年化波动率

# 时间调整
days_per_year = 252
var_95_1d = position * 1.645 * annual_vol * math.sqrt(1 / days_per_year)
var_99_10d = position * 2.326 * annual_vol * math.sqrt(10 / days_per_year)

result = {
    'var_95_1d': round(var_95_1d, 2),    # 95%一天VaR
    'var_99_10d': round(var_99_10d, 2)   # 99%十天VaR
}

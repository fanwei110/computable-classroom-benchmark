import math

# 输入参数
annual_vol = 0.24
position = 2_700_000
trading_days = 252
z_score_95 = 1.645  # 95%置信水平的Z-score

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 计算95%的一日VaR
var_95_1d = position * daily_vol * z_score_95

# 存储结果
result = {
    'var_95_1d': round(var_95_1d, 2)
}

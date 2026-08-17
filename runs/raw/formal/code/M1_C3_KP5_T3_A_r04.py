import math

# 参数
annual_vol = 0.24
position = 2_700_000
days = 252
z_score_95 = 1.64485  # 95%置信水平的正态分布分位数

# 计算日波动率
daily_vol = annual_vol / math.sqrt(days)

# 计算95%的一日VaR
var_95_1d = position * daily_vol * z_score_95

# 存入结果字典
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数
}

print(result)

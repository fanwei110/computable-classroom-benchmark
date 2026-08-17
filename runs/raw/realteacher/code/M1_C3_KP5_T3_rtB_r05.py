import math

# 输入参数
annual_vol = 0.24
position = 2_700_000
trading_days = 252
confidence_level = 0.95

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 95%置信水平下的Z值（单尾）
z_score = 1.645

# 计算VaR
var_95_1d = position * z_score * daily_vol

# 存入结果字典
result = {
    'var_95_1d': round(var_95_1d, 2)
}

print(result)

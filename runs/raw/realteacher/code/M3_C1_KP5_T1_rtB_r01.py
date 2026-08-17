import math

# 已知参数
position = 1850000
annual_vol = 0.218

# 一般假设一年有252个交易日
trading_days = 252

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# Z-score 常量
z_95 = 1.6448536269514722  # 95%置信度
z_99 = 2.3263478740408408  # 99%置信度

# 计算 95% 的一日 VaR
var_95_1d = position * daily_vol * z_95

# 计算 99% 的十日 VaR
# 10日波动率 = 日波动率 * sqrt(10)
var_99_10d = position * daily_vol * z_99 * math.sqrt(10)

# 按照契约存入字典，保留两位小数（通常货币单位保留两位）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 如果需要直接查看结果
print(result)

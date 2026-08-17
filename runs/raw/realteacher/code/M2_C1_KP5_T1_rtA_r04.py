import math

# 参数
position = 1_850_000  # 头寸
sigma_annual = 0.218  # 年化波动率
trading_days = 252

# 置信水平对应的 Z 值 (单尾)
z_95 = 1.6448536269514722
z_99 = 2.3263478740408408

# 1天波动率
sigma_1d = sigma_annual / math.sqrt(trading_days)
# 10天波动率
sigma_10d = sigma_annual * math.sqrt(10 / trading_days)

# VaR 计算
var_95_1d = position * sigma_1d * z_95
var_99_10d = position * sigma_10d * z_99

# 存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

import math

# 输入参数
position = 1_850_000        # 头寸价值
sigma_annual = 0.218        # 年化波动率
trading_days = 252          # 一年交易日数

# 置信水平对应的正态分布分位数
z_95 = 1.6448536269514722   # 95% 单尾
z_99 = 2.3263478740408408   # 99% 单尾

# 日波动率
sigma_daily = sigma_annual / math.sqrt(trading_days)

# 计算 VaR
var_95_1d = position * sigma_daily * z_95
var_99_10d = position * sigma_annual * math.sqrt(10 / trading_days) * z_99

# 结果字典（保留两位小数）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

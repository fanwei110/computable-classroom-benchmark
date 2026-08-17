import math

# 输入参数
position = 1850000  # 185万
annual_vol = 0.218  # 年化波动率21.8%

# 假设一年有252个交易日，计算日波动率
daily_vol = annual_vol / math.sqrt(252)

# 正态分布分位数 (Z-score)
# 95%置信度对应的分位数
z_95 = 1.6449 
# 99%置信度对应的分位数
z_99 = 2.3263

# 计算 95% 1天的VaR
var_95_1d = position * z_95 * daily_vol * math.sqrt(1)

# 计算 99% 10天的VaR
var_99_10d = position * z_99 * daily_vol * math.sqrt(10)

# 按照输出契约存入字典，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

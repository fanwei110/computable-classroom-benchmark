import math

# 已知参数
position = 2700000  # 270万元，转换为元
annual_vol = 0.24   # 年化波动率 24%
z_95 = 1.64485      # 95%置信水平对应的正态分布分位数（Z值）
trading_days = 252  # 假设一年252个交易日（金融市场惯例）

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 计算95%一日VaR
var_95_1d = position * z_95 * daily_vol

# 按照输出契约存入字典，结果保留两位小数
result = {'var_95_1d': round(var_95_1d, 2)}

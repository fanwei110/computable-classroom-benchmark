import math

# 给定参数
position = 1850000  # 仓位：185万
annual_vol = 0.218  # 年化波动率：21.8%
trading_days = 252  # 假设一年有252个交易日（金融市场标准假设）

# 将年化波动率转换为日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 正态分布分位数 (Z-score)
z_95 = 1.64485  # 95%置信度
z_99 = 2.32635  # 99%置信度

# 计算 95% 置信度、1天持有期的 VaR
# 公式: VaR = 仓位 * Z_95 * 日波动率 * sqrt(1)
var_95_1d = position * z_95 * daily_vol * math.sqrt(1)

# 计算 99% 置信度、10天持有期的 VaR
# 公式: VaR = 仓位 * Z_99 * 日波动率 * sqrt(10)
var_99_10d = position * z_99 * daily_vol * math.sqrt(10)

# 按照输出契约存入字典，保留两位小数（金融惯例）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

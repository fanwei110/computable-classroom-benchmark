import numpy as np
from scipy.stats import norm

# 参数
position = 1_850_000  # 仓位（万元？题目是185万，即为1,850,000）
annual_vol = 0.218    # 年化波动率 21.8%
trading_days = 252    # 假设一年252个交易日

# 置信水平对应的Z值（单尾）
z_95 = norm.ppf(0.95)  # 1.6448536269514722
z_99 = norm.ppf(0.99)  # 2.3263478740408408

# 计算VaR
var_95_1d = position * z_95 * annual_vol * np.sqrt(1 / trading_days)
var_99_10d = position * z_99 * annual_vol * np.sqrt(10 / trading_days)

# 结果存入字典，四舍五入保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

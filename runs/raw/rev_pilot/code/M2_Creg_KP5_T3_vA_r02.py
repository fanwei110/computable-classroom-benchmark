import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 2_700_000        # 头寸价值（元）
annual_volatility = 0.24         # 年化波动率
confidence_level = 0.95          # 置信水平
trading_days_per_year = 252      # 年交易日数

# 计算一日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 标准正态分布下对应置信水平的分位数（z值）
z_score = norm.ppf(confidence_level)

# 计算一日 VaR（绝对值，表示损失）
var_95_1d = position_value * daily_volatility * z_score

# 结果存入字典
result = {'var_95_1d': var_95_1d}

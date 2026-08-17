import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化收益波动率

# 常数
days_in_year = 252          # 交易日天数（通常假设一年有252个交易日）

# 计算日收益波动率
daily_volatility = annual_volatility / np.sqrt(days_in_year)

# (i) 计算95%置信水平下的1日VaR
confidence_level_95 = 0.95
z_score_95 = norm.ppf(confidence_level_95)
var_95_1d = position_value * z_score_95 * daily_volatility

# (ii) 计算99%置信水平下的10日VaR
confidence_level_99 = 0.99
z_score_99 = norm.ppf(confidence_level_99)
ten_day_volatility = daily_volatility * np.sqrt(10)
var_99_10d = position_value * z_score_99 * ten_day_volatility

# 将结果存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 输出结果（可选，题目未要求打印）
print(result)

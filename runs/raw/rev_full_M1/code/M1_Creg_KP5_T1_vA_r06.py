import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化收益波动率

# 常数
days_in_year = 252          # 交易日天数（通常假设一年有252个交易日）

# 计算日收益波动率
daily_volatility = annual_volatility / np.sqrt(days_in_year)

# (i) 95% 一日 VaR
z_score_95 = norm.ppf(0.95)  # 95%置信水平的z值
var_95_1d = position_value * z_score_95 * daily_volatility

# (ii) 99% 十日 VaR
z_score_99 = norm.ppf(0.99)  # 99%置信水平的z值
ten_day_volatility = daily_volatility * np.sqrt(10)  # 十日波动率
var_99_10d = position_value * z_score_99 * ten_day_volatility

# 结果存储
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 输出结果（可选，用于验证）
print("95% 一日 VaR:", result['var_95_1d'])
print("99% 十日 VaR:", result['var_99_10d'])

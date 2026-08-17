import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化波动率（21.8%）

# 1. 年化波动率换算到一日波动率（假设一年有252个交易日）
trading_days_per_year = 252
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 计算正态分位数（Z-score）
confidence_95 = 0.95
confidence_99 = 0.99
z_95 = norm.ppf(1 - confidence_95)  # 95%置信水平对应的Z值
z_99 = norm.ppf(1 - confidence_99)  # 99%置信水平对应的Z值

# 3. 计算VaR
# (i) 95% 一日VaR
var_95_1d = position_value * z_95 * daily_volatility

# (ii) 99% 十日VaR（假设波动率随时间平方根缩放）
ten_day_volatility = daily_volatility * np.sqrt(10)
var_99_10d = position_value * z_99 * ten_day_volatility

# 4. 结果存入字典（四舍五入到整数元）
result = {
    'var_95_1d': round(var_95_1d),
    'var_99_10d': round(var_99_10d)
}

print(result)

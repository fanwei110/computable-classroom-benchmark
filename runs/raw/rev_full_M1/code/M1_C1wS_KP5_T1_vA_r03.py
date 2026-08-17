import numpy as np
from scipy.stats import norm

# 输入参数
position = 1_850_000          # 头寸（人民币元）
annual_volatility = 0.218     # 年化波动率（21.8%）

# 1. 年化波动率换算到一日波动率
trading_days_per_year = 252
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 正态分位数
z_95 = norm.ppf(0.95)         # 95% 置信水平对应的 z 值
z_99 = norm.ppf(0.99)         # 99% 置信水平对应的 z 值

# 3. 计算 VaR
var_95_1d = position * daily_volatility * z_95
var_99_10d = position * (daily_volatility * np.sqrt(10)) * z_99

# 4. 结果存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

print(result)

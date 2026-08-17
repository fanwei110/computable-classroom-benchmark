import numpy as np
from scipy.stats import norm

# 输入参数
position = 1_850_000  # 仓位（人民币）
annual_volatility = 0.218  # 年化波动率
confidence_95 = 0.95
confidence_99 = 0.99
days_1d = 1
days_10d = 10

# 1. 年化波动率换算到日波动率（假设252个交易日/年）
trading_days_per_year = 252
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 计算正态分位数（Z-score）
z_95 = norm.ppf(1 - confidence_95)  # 95%置信水平对应的Z值
z_99 = norm.ppf(1 - confidence_99)  # 99%置信水平对应的Z值

# 3. 计算 VaR
# 一天 95% VaR
var_95_1d = position * z_95 * daily_volatility

# 十天 99% VaR（时间平方根法则缩放）
var_99_10d = position * z_99 * daily_volatility * np.sqrt(days_10d)

# 4. 结果存储（人民币，保留2位小数）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 输出结果（可选，便于调试）
print("计算结果:", result)

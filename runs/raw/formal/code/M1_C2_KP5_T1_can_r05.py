import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000  # 头寸价值（元）
annual_volatility = 0.218   # 年化波动率（21.8%）

# 1. 年化波动率换算到一日波动率（假设一年252个交易日）
daily_volatility = annual_volatility / np.sqrt(252)

# 2. 计算正态分位数（Z-score）
z_95 = norm.ppf(0.05)      # 95%置信水平对应的分位数（单尾）
z_99 = norm.ppf(0.01)      # 99%置信水平对应的分位数（单尾）

# 3. 计算 VaR
# (i) 95% 一日 VaR
var_95_1d = position_value * (-z_95) * daily_volatility

# (ii) 99% 十日 VaR
# 十日波动率 = 一日波动率 * sqrt(10)
ten_day_volatility = daily_volatility * np.sqrt(10)
var_99_10d = position_value * (-z_99) * ten_day_volatility

# 4. 结果存入字典（四舍五入到整数元）
result = {
    'var_95_1d': round(var_95_1d),
    'var_99_10d': round(var_99_10d)
}

# 输出结果（可选，用于验证）
print(result)

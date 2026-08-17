import numpy as np
from scipy.stats import norm

# 输入参数
annual_volatility = 0.24          # 年化波动率 24%
position_size = 2_700_000         # 头寸金额 2,700,000 元
confidence_level = 0.95           # 置信水平 95%

# 1. 年化波动率换算为一日波动率
# 假设一年有 252 个交易日
trading_days_per_year = 252
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 95% 正态分位数（单尾）
z_score = norm.ppf(1 - confidence_level)

# 3. 计算一日 VaR
var_95_1d = position_size * daily_volatility * z_score

# 存储结果
result = {
    'var_95_1d': round(var_95_1d, 2)   # 保留两位小数
}

print(result)

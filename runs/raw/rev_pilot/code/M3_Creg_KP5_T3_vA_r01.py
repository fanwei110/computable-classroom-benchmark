import numpy as np
from scipy import stats

# 已知参数
annual_volatility = 0.24
position_value = 2700000
confidence_level = 0.95

# 假设一年有252个交易日，计算日波动率
trading_days_per_year = 252
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 计算95%置信水平下的标准正态分布分位数 (单尾)
z_score = stats.norm.ppf(confidence_level)

# 计算参数法 95% 一日 VaR
var_95_1d = z_score * daily_volatility * position_value

# 按照输出契约存入字典
result = {
    'var_95_1d': var_95_1d
}

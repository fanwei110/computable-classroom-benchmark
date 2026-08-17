import numpy as np
from scipy import stats

# 已知参数
annual_volatility = 0.24          # 24% 年化波动率
position = 2_700_000              # 头寸 2,700,000 元
confidence_level = 0.95           # 95% 置信水平
trading_days_per_year = 252       # 年化交易天数

# 计算日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 95%置信水平对应的z-score（单尾）
z_score = stats.norm.ppf(confidence_level)

# 计算VaR
var_95_1d = position * daily_volatility * z_score

# 按要求存入result字典
result = {
    'var_95_1d': var_95_1d
}

print(f"95% 一日 VaR = {result['var_95_1d']:,.2f} 元")

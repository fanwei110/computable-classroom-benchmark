import numpy as np
from scipy.stats import norm

# 输入参数
annualized_volatility = 0.24  # 年化波动率 24%
position_value = 2_700_000   # 头寸价值 2,700,000 元
confidence_level = 0.95      # 置信水平 95%

# 计算日波动率（年化波动率转换为日波动率）
trading_days_per_year = 252
daily_volatility = annualized_volatility / np.sqrt(trading_days_per_year)

# 计算 95% 一日 VaR（正态分布假设）
z_score = norm.ppf(1 - confidence_level)  # 95% 置信水平对应的 z 分数
var_95_1d = position_value * daily_volatility * z_score

# 将结果存入字典
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数
}

# 输出结果（可选，用于验证）
print(result)

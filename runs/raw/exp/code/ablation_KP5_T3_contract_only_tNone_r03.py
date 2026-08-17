import numpy as np
from scipy.stats import norm

# 给定参数
annual_volatility = 0.24  # 年化波动率 24%
position = 2_700_000      # 头寸 2,700,000 元
confidence_level = 0.95   # 置信水平 95%
days_per_year = 252       # 一年交易天数（常规假设）

# 计算一日波动率（从年化转换）
daily_volatility = annual_volatility / np.sqrt(days_per_year)

# 计算95%置信水平下的标准差倍数（单尾，因为VaR只关心亏损侧）
z_score = norm.ppf(confidence_level)   # 约 1.64485

# 计算 VaR（假定收益率均值为0，最常用）
# VaR = 头寸 * 一日波动率 * z_score
var_95_1d = position * daily_volatility * z_score

# 输出结果存入字典，严格按要求键名
result = {
    'var_95_1d': round(var_95_1d, 2)   # 保留两位小数，便于查看
}

# 打印确认（符合输出契约）
print(result)

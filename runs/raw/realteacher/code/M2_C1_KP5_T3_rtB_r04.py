import numpy as np
from scipy.stats import norm

# 参数
annual_vol = 0.24
position = 2_700_000  # 270万
confidence = 0.95
days_per_year = 252

# 计算一日波动率
daily_vol = annual_vol / np.sqrt(days_per_year)

# 95%置信度下的Z分数（单尾，5%损失分位数取负值，VaR取正数）
z_score = norm.ppf(1 - confidence)  # 注意：ppf(0.05) 为负值，取绝对值
var_95_1d = position * daily_vol * abs(z_score)

result = {'var_95_1d': round(var_95_1d, 2)}

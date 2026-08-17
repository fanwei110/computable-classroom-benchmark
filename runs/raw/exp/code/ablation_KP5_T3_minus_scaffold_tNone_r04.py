import numpy as np
from scipy.stats import norm

# 给定参数
vol_annual = 0.24   # 年化波动率 24%
position = 2_700_000  # 头寸金额 2,700,000 元
confidence = 0.95    # 置信水平 95%
days_per_year = 252  # 每年交易日数

# 计算一日波动率（年化 -> 日）
vol_daily = vol_annual / np.sqrt(days_per_year)

# 单尾正态分位数，95% 置信水平对应 z = norm.ppf(0.95) = 约 1.64485
z = norm.ppf(confidence)

# 约定：短期限下均值取零，VaR = 损失金额（正值）
# VaR = z * sigma_daily * position
var_95_1d = z * vol_daily * position

# 输出结果字典
result = {
    'var_95_1d': var_95_1d
}

print("95% 一日 VaR 金额（元）:", round(result['var_95_1d'], 2))

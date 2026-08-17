import math
from scipy.stats import norm

# 给定参数
position = 1_850_000         # 头寸
sigma_annual = 0.218        # 年化波动率
days = 252                  # 年交易日数

# 波动率缩放
sigma_day = sigma_annual / math.sqrt(days)
sigma_10d = sigma_annual * math.sqrt(10 / days)

# 置信水平对应的 z 值（左尾分位数的绝对值）
z_95 = -norm.ppf(0.05)      # 约 1.64485
z_99 = -norm.ppf(0.01)      # 约 2.32635

# 参数法 VaR（损失金额, 正数）
var_95_1d = position * z_95 * sigma_day
var_99_10d = position * z_99 * sigma_10d

result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

import numpy as np
from scipy.stats import norm

# 给定参数
年化波动率 = 0.24   # 24%
头寸 = 2_700_000   # 元
置信水平 = 0.95
交易日数 = 1

# 参数法（delta-normal）计算一日VaR
# 单尾正态分位数（损失侧）
z = norm.ppf(置信水平)   # 95% 单尾分位数 ≈ 1.64485

# 日波动率 = 年化波动率 / sqrt(252)
日波动率 = 年化波动率 / np.sqrt(252)

# 短期 VaR 约定均值视为0
var_95_1d = z * 日波动率 * 头寸

# 输出为字典
result = {
    'var_95_1d': round(var_95_1d, 2)   # 保留两位小数，金额单位：元
}

print(result)

import numpy as np
from scipy.stats import norm

# 给定参数
vol_annual = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸金额 2,700,000 元
confidence_level = 0.95    # 95% 置信水平
days_per_year = 252        # 每年交易日数

# 计算一日波动率（去年化）
vol_daily = vol_annual / np.sqrt(days_per_year)

# 95% 单尾正态分位数
z_95 = norm.ppf(confidence_level)   # ≈ 1.64485

# 短期 VaR 均值取零：VaR = - (0 + z * sigma) * 头寸 = z * sigma * 头寸
# 注意教材约定：VaR 报告为正的损失金额，因此直接用 z * sigma * position
var_95_1d = z_95 * vol_daily * position

# 输出结果字典
result = {
    'var_95_1d': var_95_1d
}

# 打印结果（便于课堂展示）
print(f"95% 一日 VaR = {result['var_95_1d']:,.2f} 元")

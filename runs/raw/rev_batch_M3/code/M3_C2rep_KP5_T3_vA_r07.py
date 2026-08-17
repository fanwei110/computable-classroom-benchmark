import numpy as np
from scipy.stats import norm

# ===================== 参数设定 =====================
sigma_annual = 0.24          # 年化波动率 24%
position_value = 2_700_000   # 头寸金额 2,700,000 元
confidence_level = 0.95      # 95% 置信水平

# 假设：按照市场惯例，一年按 252 个交易日计算
# 平方根时间法则：日波动率 = 年化波动率 / sqrt(交易日天数)
trading_days_per_year = 252

# ===================== 步骤1：换算一日波动率 =====================
sigma_daily = sigma_annual / np.sqrt(trading_days_per_year)

# ===================== 步骤2：套用 95% 正态分位数 =====================
# 参数法（Delta-Normal）假设损益分布服从正态分布，获取上侧分位数
z_score_95 = norm.ppf(confidence_level)

# ===================== 步骤3：计算 95% 一日 VaR =====================
# VaR = 头寸金额 × 一日波动率 × 对应分位数
var_95_1d = position_value * sigma_daily * z_score_95

# ===================== 输出契约 =====================
result = {
    'var_95_1d': var_95_1d
}

# （课堂展示辅助打印，非契约必须但便于教师投屏讲解）
print(f"一日波动率: {sigma_daily:.6f}")
print(f"95% 正态分位数 (Z值): {z_score_95:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")

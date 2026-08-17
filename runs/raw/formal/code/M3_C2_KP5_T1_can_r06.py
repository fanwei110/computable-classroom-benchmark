import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
position_value = 1_850_000  # 头寸价值（人民币元）
annual_vol = 0.218          # 年化收益波动率
trading_days_per_year = 252 # 假设一年有252个交易日（市场惯例）

# ==================== 步骤1：年化波动率换算到一日期限 ====================
# 假设日收益独立同分布，日波动率 = 年化波动率 / sqrt(年交易日数)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ==================== 步骤2：套用正态分位数 ====================
# Delta-normal模型下，假设收益服从正态分布
z_95 = norm.ppf(0.95)  # 95%置信水平下的正态分位数
z_99 = norm.ppf(0.99)  # 99%置信水平下的正态分位数

# ==================== 步骤3：计算VaR并缩放期限 ====================
# (i) 95% 一日 VaR
var_95_1d = position_value * z_95 * daily_vol

# 期限缩放：T日波动率 = 1日波动率 * sqrt(T)
ten_day_vol = daily_vol * np.sqrt(10)

# (ii) 99% 十日 VaR
var_99_10d = position_value * z_99 * ten_day_vol

# ==================== 步骤4：填充结果 ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# （投屏辅助打印，便于课堂展示）
print(f"日波动率: {daily_vol:.6f}")
print(f"正态分位数 (95%): {z_95:.6f}")
print(f"正态分位数 (99%): {z_99:.6f}")
print("-" * 30)
print(f"95% 一日 VaR: ¥{result['var_95_1d']:,.2f}")
print(f"99% 十日 VaR: ¥{result['var_99_10d']:,.2f}")


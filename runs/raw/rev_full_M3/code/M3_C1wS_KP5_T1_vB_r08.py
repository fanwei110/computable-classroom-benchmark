import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
position = 1850000       # 仓位：185万人民币
annual_vol = 0.218       # 年化波动率：21.8%

# 假设：按照金融市场标准惯例，一年包含252个交易日
trading_days_per_year = 252

# ==================== 步骤1：换算一日期限波动率 ====================
# 参数法下，时间的平方根法则：sigma_daily = sigma_annual / sqrt(T)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ==================== 步骤2：套用正态分位数 ====================
# 使用 scipy 获取标准正态分布的逆累积分布函数（分位数）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# ==================== 步骤3：计算VaR并缩放期限 ====================
# VaR = Position × Z_alpha × sigma
# 1天、95%置信水平的VaR
var_95_1d = position * z_95 * daily_vol

# 10天、99%置信水平的VaR
# 期限缩放法则：sigma_T = sigma_1 × sqrt(T)
var_99_10d = position * z_99 * daily_vol * np.sqrt(10)

# ==================== 步骤4：填充结果 ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 投屏展示辅助输出
print(f"假设一年 {trading_days_per_year} 个交易日：")
print(f"日度波动率: {daily_vol:.6%}")
print(f"正态分位数 Z(95%): {z_95:.4f}, Z(99%): {z_99:.4f}")
print("-" * 40)
print(f"95% 1天  VaR: {result['var_95_1d']:>12,.2f} 人民币")
print(f"99% 10天 VaR: {result['var_99_10d']:>12,.2f} 人民币")

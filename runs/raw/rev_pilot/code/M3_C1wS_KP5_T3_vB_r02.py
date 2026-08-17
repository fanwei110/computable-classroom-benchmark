import numpy as np
from scipy.stats import norm

# ==================== 参数设置 ====================
annual_vol = 0.24          # 年化波动率 24%
position = 2700000         # 头寸金额 270万
confidence_level = 0.95    # 置信水平 95%
trading_days = 252         # 假设一年有252个交易日（证券投资学标准假设）

# ==================== 步骤 1：年化波动率换算到一日期限 ====================
# 使用平方根时间法则（Square-root-of-time rule）：sigma_daily = sigma_annual / sqrt(T)
daily_vol = annual_vol / np.sqrt(trading_days)

# ==================== 步骤 2：套用 95% 正态分位数 ====================
# 使用 scipy 获取标准正态分布下 95% 的单尾分位数（Z-score）
z_score_95 = norm.ppf(confidence_level)

# ==================== 步骤 3：计算 95% 一日 VaR 金额 ====================
# VaR = Z-score * 日波动率 * 头寸金额
var_95_1d_value = z_score_95 * daily_vol * position

# ==================== 输出契约 ====================
result = {
    'var_95_1d': var_95_1d_value
}

# 课堂投屏辅助打印（便于教师讲解步骤，不影响result字典契约）
print(f"步骤1 - 日波动率: {annual_vol} / sqrt({trading_days}) = {daily_vol:.6f}")
print(f"步骤2 - 95%正态分位数(Z值): {z_score_95:.6f}")
print(f"步骤3 - 95%一日VaR: {z_score_95:.6f} * {daily_vol:.6f} * {position} = {var_95_1d_value:.2f} 元")
print("-" * 40)
print(f"最终结果 result = {result}")

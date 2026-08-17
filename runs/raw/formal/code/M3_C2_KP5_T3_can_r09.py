import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
annual_vol = 0.24              # 年化波动率 24%
position_value = 2_700_000     # 头寸金额 2,700,000 元
confidence_level = 0.95        # 95% 置信水平

# 假设：一年有 252 个交易日（业界标准假设）
trading_days_per_year = 252

# ==================== 步骤1：年化波动率换算到一日期限 ====================
# 使用平方根法则：
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ==================== 步骤2：套用 95% 正态分位数 ====================
# 参数法假设损益服从正态分布，获取95%的单尾置信度对应的Z分数
z_score_95 = norm.ppf(confidence_level)

# ==================== 步骤3：计算 95% 一日 VaR 金额 ====================
# VaR = 头寸金额 × 一日波动率 × Z分数
var_95_1d = position_value * daily_vol * z_score_95

# ==================== 输出契约 ====================
result = {
    'var_95_1d': var_95_1d
}

# 课堂投屏展示辅助信息
print(f"=== 在险价值计算过程 ===")
print(f"年化波动率: {annual_vol:.2%}")
print(f"一年交易日假设: {trading_days_per_year} 天")
print(f"一日波动率: {daily_vol:.4%}")
print(f"95% 正态分位数: {z_score_95:.4f}")
print(f"头寸金额: {position_value:,.2f} 元")
print(f"-------------------------")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print(f"\n字典输出结果: {result}")

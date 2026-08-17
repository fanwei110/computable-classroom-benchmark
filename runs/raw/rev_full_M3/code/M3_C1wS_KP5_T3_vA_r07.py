import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
annual_vol = 0.24          # 年化波动率 24%
position = 2700000         # 头寸金额 270万元
confidence_level = 0.95    # 95% 置信水平
trading_days = 252         # 假设一年有252个交易日（市场惯例）

# ==================== 步骤1：年化波动率换算到一日期限 ====================
# 根据平方根法则，日波动率 = 年化波动率 / sqrt(一年内的交易天数)
daily_vol = annual_vol / np.sqrt(trading_days)

# ==================== 步骤2：套用 95% 正态分位数 ====================
# 使用 scipy 获取标准正态分布的 95% 分位数
z_score_95 = norm.ppf(confidence_level)

# ==================== 步骤3：计算 95% 一日 VaR ====================
# VaR = 头寸金额 × 分位数 × 日波动率
var_95_1d = position * z_score_95 * daily_vol

# ==================== 输出契约 ====================
result = {
    'var_95_1d': var_95_1d
}

# （以下为课堂投屏辅助展示，非契约要求但有助于教学演示）
print(f"=== 在险价值计算演示 ===")
print(f"年化波动率: {annual_vol:.2%}")
print(f"日化波动率: {daily_vol:.4%}")
print(f"95%正态分位数: {z_score_95:.4f}")
print(f"头寸金额: {position:,.2f} 元")
print(f"计算得出的 95% 一日 VaR: {result['var_95_1d']:,.2f} 元")

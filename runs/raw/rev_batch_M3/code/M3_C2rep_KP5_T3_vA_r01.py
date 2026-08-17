import numpy as np
from scipy.stats import norm

# ==================== 假设与输入 ====================
# 题目未指明一年中的交易日天数，采用金融市场惯例假设一年有 252 个交易日
trading_days_per_year = 252

# 已知条件
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸金额 2,700,000 元
confidence_level = 0.95    # 95% 置信水平

# ==================== 步骤 1：年化波动率换算到一日期限 ====================
# 根据平方根法则：日波动率 = 年化波动率 / sqrt(一年交易日天数)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ==================== 步骤 2：套用 95% 正态分位数 ====================
# 使用 Delta-Normal 参数法，获取标准正态分布的 95% 分位数
z_score_95 = norm.ppf(confidence_level)

# ==================== 步骤 3：计算 VaR 金额 ====================
# VaR = 头寸金额 × 日波动率 × 对应分位数
var_95_1d = position * daily_vol * z_score_95

# ==================== 输出契约 ====================
# 将结果存入名为 result 的字典，键名严格为 'var_95_1d'
result = {
    'var_95_1d': var_95_1d
}

# 课堂投屏打印展示（可选，便于教师讲解）
print(f"假设一年 {trading_days_per_year} 个交易日：")
print(f"日波动率: {daily_vol:.6f}")
print(f"95% 正态分位数: {z_score_95:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")
print(f"\n最终结果字典: {result}")

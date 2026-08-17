import numpy as np
from scipy.stats import norm

# ==================== 已知参数 ====================
sigma_annual = 0.24          # 年化波动率 (24%)
position_value = 2700000     # 头寸金额 (元)
trading_days = 252           # 年化交易日天数
confidence_level = 0.95      # 置信水平 (95%)

# ==================== 步骤1：去年化波动率 ====================
# 波动率按 sqrt(252) 缩放
sigma_daily = sigma_annual / np.sqrt(trading_days)

# ==================== 步骤2：计算单尾正态分位数 ====================
# 使用 scipy 计算单尾 95% 对应的正态分位数，均值取零
z_score_95 = norm.ppf(confidence_level)

# ==================== 步骤3：计算 VaR ====================
# 短期限下均值取零，VaR 报告为正的损失金额
# VaR = 头寸金额 × 分位数 × 日波动率
var_95_1d = position_value * z_score_95 * sigma_daily

# ==================== 输出结果 ====================
result = {
    'var_95_1d': var_95_1d
}

# 供教师投屏展示的打印输出（可选，便于课堂演示）
print(f"日波动率: {sigma_daily:.6f}")
print(f"95% 正态分位数: {z_score_95:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")
print(f"result 字典: {result}")

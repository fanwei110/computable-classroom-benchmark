import numpy as np
from scipy.stats import norm

# ==================== 假设与输入参数 ====================
# 头寸价值（人民币）
position_value = 1_850_000.0

# 年化收益波动率
annual_volatility = 0.218

# 假设：一年有252个交易日（金融学通用假设，题目未指明）
trading_days_per_year = 252

# ==================== 步骤1：年化波动率换算到一日期限 ====================
# 参数法下，波动率随时间的平方根缩放：sigma_1d = sigma_ann / sqrt(T)
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# ==================== 步骤2：套用正态分位数 ====================
# 95%和99%置信水平下的正态分布单尾分位数（取绝对值表示损失）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# ==================== 步骤3：计算VaR并缩放 ====================
# (i) 95% 一日 VaR
# VaR = 头寸价值 × 一日波动率 × 分位数
var_95_1d = position_value * daily_volatility * z_95

# (ii) 99% 十日 VaR
# 十日波动率缩放：sigma_10d = sigma_1d * sqrt(10)
var_99_10d = position_value * daily_volatility * np.sqrt(10) * z_99

# 保留两位小数（以人民币报告）
var_95_1d_rmb = round(var_95_1d, 2)
var_99_10d_rmb = round(var_99_10d, 2)

# ==================== 步骤4：填充结果 ====================
result = {
    'var_95_1d': var_95_1d_rmb,
    'var_99_10d': var_99_10d_rmb
}

# 课堂投屏展示打印
print(f"假设条件：一年 = {trading_days_per_year} 个交易日")
print(f"年化波动率: {annual_volatility:.2%} -> 日波动率: {daily_volatility:.4%}")
print(f"正态分位数: Z(95%) = {z_95:.4f}, Z(99%) = {z_99:.4f}")
print("-" * 40)
print(f"(i) 95% 一日 VaR: ￥{var_95_1d_rmb:,.2f}")
print(f"(ii) 99% 十日 VaR: ￥{var_99_10d_rmb:,.2f}")


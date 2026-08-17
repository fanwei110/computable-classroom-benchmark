import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24        # 年化波动率 24%
position = 2_700_000     # 头寸金额 2,700,000 元
confidence_level = 0.95  # 置信水平 95%
trading_days = 252       # 每年交易日数

# 步骤1：去年化 —— 日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 步骤2：单尾 95% 正态分位数，均值取零
z_score = norm.ppf(confidence_level)   # 95% 单尾分位数 ≈ 1.64485

# 步骤3：计算 VaR (正的人民币金额)
# VaR = 头寸 × 日波动率 × 分位数  (均值为0)
var_95_1d = position * daily_vol * z_score

# 输出契约
result = {
    'var_95_1d': var_95_1d
}

# 打印结果（供课堂展示）
print(f"95% 一日 VaR = {var_95_1d:,.2f} 元")

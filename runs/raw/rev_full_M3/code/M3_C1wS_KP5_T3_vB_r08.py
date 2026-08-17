import numpy as np
from scipy.stats import norm

# ---------------- 假设与输入参数 ----------------
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 270万
confidence_level = 0.95    # 95% 置信水平
trading_days = 252         # 假设一年有252个交易日（国际通用参数法自洽假设）

# ---------------- 步骤 1 ----------------
# 将年化波动率换算到一日期限（使用平方根时间法则）
daily_vol = annual_vol / np.sqrt(trading_days)

# ---------------- 步骤 2 ----------------
# 套用 95% 正态分位数（单尾）
z_score_95 = norm.ppf(confidence_level)

# ---------------- 步骤 3 ----------------
# 计算 95% 一日 VaR 金额 (Delta-Normal 参数法)
# VaR = 头寸 * 日波动率 * 分位数
var_95_1d = position * daily_vol * z_score_95

# ---------------- 输出契约 ----------------
result = {
    'var_95_1d': var_95_1d
}

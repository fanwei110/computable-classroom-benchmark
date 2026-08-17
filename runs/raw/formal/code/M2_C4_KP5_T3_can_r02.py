import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000.0     # 头寸金额（元）
trading_days = 252         # 年交易日
confidence = 0.95          # VaR 置信水平

# 1. 去年化：日波动率 = 年化波动率 / sqrt(252)
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 单尾 95% 正态分位数（左尾 5% 分位数对应损失侧）
z_alpha = norm.ppf(1 - confidence)  # 标准正态的 5% 分位数，为负值

# 3. 一日 VaR（报告为正的损失金额，均值取零）
var_95_1d = position * daily_vol * abs(z_alpha)

# 输出契约
result = {
    'var_95_1d': var_95_1d
}

print(result)

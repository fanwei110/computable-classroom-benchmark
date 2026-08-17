import numpy as np
from scipy.stats import norm

# ---- 题目已知参数 ----
annual_vol = 0.24          # 年化波动率
position   = 2_700_000     # 头寸金额（元）
confidence = 0.95          # 置信水平
trading_days = 252         # 一年交易日数（标准假设）

# ---- 1. 年化波动率换算为一日波动率 ----
daily_vol = annual_vol / np.sqrt(trading_days)

# ---- 2. 95% 正态分位数（左尾临界值，取绝对值表示损失金额） ----
z_alpha = abs(norm.ppf(1 - confidence))   # 等价于 norm.ppf(0.05) 的绝对值

# ---- 3. 参数法（delta-normal）计算一日 95% VaR ----
var_95_1d = position * daily_vol * z_alpha

# ---- 输出 ----
result = {'var_95_1d': var_95_1d}
print(result)

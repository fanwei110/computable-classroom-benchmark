import numpy as np
from scipy.stats import norm

# 给定参数
position_value = 2_700_000       # 头寸金额（元）
annual_vol = 0.24                # 年化波动率
confidence = 0.95                # 置信水平
trading_days = 252               # 年交易日数假设

# 1. 年化波动率换算为日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 95%置信水平下的正态分布分位数（左尾）
z_score = norm.ppf(1 - confidence)  # 对于95%置信水平，结果为负数
# VaR通常取正值，所以取绝对值
var_95_1d = position_value * daily_vol * abs(z_score)

# 3. 存入结果字典
result = {
    'var_95_1d': var_95_1d
}

# 输出结果（供教师投屏查看）
print(result)

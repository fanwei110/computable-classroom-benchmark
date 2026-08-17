import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 2,700,000 元
confidence = 0.95          # 置信水平 95%
trading_days = 252         # 每年交易日数

# 1. 去年化：年化波动率 ÷ sqrt(252)
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 单尾 95% 正态分位数（均值取零）
z = norm.ppf(confidence)   # 约 1.64485

# 3. 一日 VaR = 头寸 × 日波动率 × 分位数（正数损失）
var_95_1d = position * daily_vol * z

# 存入 result 字典
result = {
    'var_95_1d': round(var_95_1d, 2)   # 保留两位小数，更清晰
}

# 输出结果（供课堂展示）
print(result)

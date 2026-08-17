import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 2,700,000 元
confidence = 0.95          # 置信水平 95%
trading_days = 252         # 一年交易日数

# 1. 去年化：日波动率 = 年化波动率 / sqrt(252)
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 单尾 95% 正态分位数（均值取零）
z_score = norm.ppf(confidence)   # 单尾下，95% 对应的分位点

# 3. VaR = 头寸 × 日波动率 × z_score （正数损失）
var_95_1d = position * daily_vol * z_score

# 存入 result 字典
result = {
    'var_95_1d': var_95_1d
}

# 打印结果供课堂展示（保留两位小数）
print(f"日波动率（去年化后）: {daily_vol:.6f}")
print(f"95% 单尾正态分位数: {z_score:.4f}")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")

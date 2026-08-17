import numpy as np
from scipy import stats

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸金额 2,700,000 元
confidence = 0.95          # 置信水平 95%
trading_days = 252         # 每年交易日数

# 1. 去年化：年化波动率 / sqrt(252) -> 日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 单尾 95% 正态分位数（均值取零）
z = stats.norm.ppf(confidence)   # 约 1.64485

# 3. 一日 VaR = 头寸 × z × 日波动率（正数损失金额）
var_95_1d = position * z * daily_vol

# 存入 result 字典
result = {
    'var_95_1d': var_95_1d
}

# 可选：打印结果以便课堂展示
print(f"年化波动率: {annual_vol}")
print(f"日波动率: {daily_vol:.6f}")
print(f"95% 单尾正态分位数: {z:.4f}")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print(f"result = {result}")

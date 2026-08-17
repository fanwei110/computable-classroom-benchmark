import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 2,700,000 元
confidence = 0.95          # 置信水平 95%
trading_days = 252         # 每年交易日数

# 1. 去年化：年化波动率 -> 一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 单尾 95% 正态分位数（均值取零）
z = norm.ppf(confidence)   # 约 1.64485

# 3. 一日 VaR（正数损失金额）
var_95_1d = z * daily_vol * position

# 存入 result 字典
result = {
    'var_95_1d': var_95_1d
}

# 输出结果（课堂展示用）
print(f"年化波动率: {annual_vol:.4f}")
print(f"一日波动率: {daily_vol:.6f}")
print(f"95% 单尾分位数: {z:.4f}")
print(f"头寸金额: {position:,.0f} 元")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print(f"\nresult 字典: {result}")

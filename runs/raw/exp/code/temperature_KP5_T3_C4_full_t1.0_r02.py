import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 2,700,000 元
confidence = 0.95          # 置信水平 95%
trading_days = 252         # 每年交易日数

# 1. 去年化波动率：从年化波动率计算一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 单尾95%正态分位数（均值取零）
z_score = norm.ppf(confidence)   # 约 1.64485

# 3. 计算 VaR（正数损失金额）
var_95_1d = z_score * daily_vol * position

# 存入 result 字典
result = {
    'var_95_1d': var_95_1d
}

# 输出结果（可选，方便课堂演示）
print(f"95% 一日 VaR = {result['var_95_1d']:,.2f} 元")

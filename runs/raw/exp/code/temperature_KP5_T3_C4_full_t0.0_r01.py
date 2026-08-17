import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 2,700,000 元
confidence = 0.95          # 置信水平 95%
trading_days = 252         # 每年交易日数

# 步骤1：去年化到一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 步骤2：单尾95%正态分位数（均值取零）
z = norm.ppf(confidence)   # 单尾分位数，例如 95% → 约1.645

# 步骤3：计算 VaR（正数损失金额）
var_95_1d = z * daily_vol * position

# 存入 result 字典
result = {
    'var_95_1d': var_95_1d
}

# 输出结果（教师投屏可见）
print(result)

import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 2,700,000 元
confidence = 0.95          # 置信水平 95%
trading_days = 252         # 每年交易日数

# 计算一日波动率（去年化）
daily_vol = annual_vol / np.sqrt(trading_days)

# 单尾正态分位数（95% 置信水平对应分位数约为 1.64485）
z = norm.ppf(confidence)

# 短期 VaR 假设均值为零，VaR = 头寸 × 波动率 × z
# VaR 报告为正的损失金额
var_95_1d = position * daily_vol * z

# 存入结果字典
result = {
    'var_95_1d': round(float(var_95_1d), 2)   # 保留两位小数，便于展示
}

# 输出结果（教师投屏可见）
print("95% 一日 VaR 金额（元）:", result['var_95_1d'])

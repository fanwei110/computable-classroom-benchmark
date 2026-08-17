import numpy as np
from scipy.stats import norm

# 输入参数
position = 1_850_000  # 仓位（人民币）
annual_vol = 0.218    # 年化波动率
confidence_95 = 0.95  # 95% 置信水平
confidence_99 = 0.99  # 99% 置信水平

# 1. 年化波动率换算到日波动率（假设252个交易日/年）
trading_days_per_year = 252
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# 2. 计算正态分位数（Z-score）
z_95 = norm.ppf(1 - confidence_95)  # 95% 置信水平对应的 Z 值
z_99 = norm.ppf(1 - confidence_99)  # 99% 置信水平对应的 Z 值

# 3. 计算 VaR
# 95% 置信水平，1 天 VaR
var_95_1d = position * daily_vol * z_95

# 99% 置信水平，10 天 VaR（波动率按 sqrt(10) 缩放）
var_99_10d = position * daily_vol * np.sqrt(10) * z_99

# 4. 结果存储（人民币，绝对值）
result = {
    'var_95_1d': abs(round(var_95_1d, 2)),
    'var_99_10d': abs(round(var_99_10d, 2))
}

# 输出结果（可选，便于调试）
print("95% 置信水平 1 天 VaR:", result['var_95_1d'], "元")
print("99% 置信水平 10 天 VaR:", result['var_99_10d'], "元")

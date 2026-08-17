import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24                # 年化波动率
position_value = 2_700_000       # 头寸价值（元）
trading_days = 252               # 假设一年交易日数

# 1. 年化波动率转一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 95% 正态分位数（标准正态分布的逆累积分布）
z_95 = norm.ppf(0.95)

# 3. 计算一日 VaR（损失取正数）
var_95_1d = position_value * daily_vol * z_95

# 输出契约
result = {'var_95_1d': var_95_1d}

# 可选打印，方便教师投屏查看（数值以元为单位）
print(f"一日 95% VaR: {var_95_1d:,.2f} 元")
print("结果字典:", result)

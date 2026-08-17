import numpy as np
from scipy.stats import norm
import pandas as pd          # 题目要求允许导入，以备不时之需
import matplotlib.pyplot as plt  # 题目要求允许导入，以备不时之需

# 输入参数
position_value = 1_850_000   # 头寸价值
annual_volatility = 0.218    # 年化波动率
trading_days = 252           # 一年交易日数假设

# 计算日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days)

# 计算十日波动率
ten_day_volatility = daily_volatility * np.sqrt(10)

# 计算分位数（标准正态分布）
z_95 = norm.ppf(0.95)   # 95% 置信水平单侧分位数
z_99 = norm.ppf(0.99)   # 99% 置信水平单侧分位数

# 计算 VaR（正数表示损失）
var_95_1d = position_value * daily_volatility * z_95
var_99_10d = position_value * ten_day_volatility * z_99

# 按要求输出字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印结果以便查看
print(result)

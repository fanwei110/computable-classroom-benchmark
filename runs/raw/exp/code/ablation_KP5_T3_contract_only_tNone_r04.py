import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

# 给定参数
position_value = 2_700_000  # 头寸价值 2,700,000 元
annual_volatility = 0.24    # 年化波动率 24%
confidence_level = 0.95     # 置信水平 95%
trading_days_per_year = 252  # 一年交易天数

# 计算一日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 使用正态分布计算VaR
# 对于正态分布，在95%置信水平下，z-score = -1.645（左尾）
z_score = stats.norm.ppf(1 - confidence_level)  # 返回左尾分位数

# VaR = 头寸价值 × 一日波动率 × z-score的绝对值
var_95_1d = -z_score * daily_volatility * position_value

# 整理结果
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数，以元为单位
}

# 输出结果
print("计算结果:")
print(f"一日VaR (95%) = {result['var_95_1d']:,.2f} 元")

# 验证计算过程
print("\n计算过程:")
print(f"头寸价值: {position_value:,.0f} 元")
print(f"年化波动率: {annual_volatility*100:.1f}%")
print(f"一日波动率: {daily_volatility*100:.2f}%")
print(f"Z-score (95%): {z_score:.4f}")
print(f"VaR绝对值: {var_95_1d:,.2f} 元")

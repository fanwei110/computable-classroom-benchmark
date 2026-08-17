import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# 参数设置
position_value = 1_850_000          # 头寸价值
annual_vol = 0.218                  # 年化收益波动率
trading_days = 252                  # 年交易日数（行业惯例）

# 波动率换算
sigma_daily = annual_vol / np.sqrt(trading_days)   # 单日波动率
sigma_10d = sigma_daily * np.sqrt(10)              # 十日波动率（独立同分布假设）

# 分位数（z值）
z_95 = norm.ppf(0.95)   # 95%置信水平对应的标准正态分位数
z_99 = norm.ppf(0.99)   # 99%置信水平对应的标准正态分位数

# Delta-Normal VaR（损失取正值）
var_95_1d = position_value * sigma_daily * z_95
var_99_10d = position_value * sigma_10d * z_99

# 按要求输出到字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

print(result)

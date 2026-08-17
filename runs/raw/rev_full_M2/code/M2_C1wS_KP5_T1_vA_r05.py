import numpy as np
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ 参数设置 ------------------
position = 1_850_000          # 头寸规模（人民币元）
annual_vol = 0.218           # 年化波动率
trading_days_per_year = 252  # 一年中的交易天数
confidence_95 = 0.95         # 95% 置信水平
confidence_99 = 0.99         # 99% 置信水平
horizon_10d = 10             # 十日期限（交易日）

# ------------------ 波动率换算 ------------------
# 假设收益率独立同分布，日波动率 = 年化波动率 / sqrt(252)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ------------------ 正态分位数 ------------------
z_95 = norm.ppf(confidence_95)  # 95% 对应的标准正态分位数
z_99 = norm.ppf(confidence_99)  # 99% 对应的标准正态分位数

# ------------------ VaR 计算 ------------------
# 1 日 VaR（95% 置信水平）
var_95_1d = position * daily_vol * z_95

# 10 日 VaR（99% 置信水平），使用平方根法则缩放
var_99_10d = position * daily_vol * np.sqrt(horizon_10d) * z_99

# ------------------ 输出结果 ------------------
result = {
    'var_95_1d': round(var_95_1d, 2),   # 保留两位小数
    'var_99_10d': round(var_99_10d, 2)
}

# 可选的打印，便于课堂查看
if __name__ == '__main__':
    print("参数法 VaR 计算结果：")
    print(f"95% 置信水平 1 日 VaR : {result['var_95_1d']:,.2f} 元")
    print(f"99% 置信水平 10 日 VaR: {result['var_99_10d']:,.2f} 元")

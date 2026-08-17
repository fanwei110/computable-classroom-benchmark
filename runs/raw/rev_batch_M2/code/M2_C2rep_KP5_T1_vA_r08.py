import numpy as np
from scipy.stats import norm

# 给定参数
position_value = 1_850_000      # 头寸价值（元）
annual_vol = 0.218              # 年化波动率
trading_days = 252              # 假设一年交易日为252天，业界常用

# 1. 计算一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 正态分位数（左尾）
z_95 = norm.ppf(0.05)  # 95%置信水平对应左尾5%分位数
z_99 = norm.ppf(0.01)  # 99%置信水平对应左尾1%分位数

# 3. 计算一日VaR (95%)，取绝对值，表示为损失的正数
var_95_1d = abs(position_value * daily_vol * z_95)

# 4. 计算十日VaR (99%)
# 方式一：先算一日VaR再按时间平方根缩放
var_99_1d = abs(position_value * daily_vol * z_99)
var_99_10d = var_99_1d * np.sqrt(10)

# 结果保存为字典，保留两位小数（人民币）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 打印输出以便课堂投屏查看
print("在险价值（VaR）计算结果：")
print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")

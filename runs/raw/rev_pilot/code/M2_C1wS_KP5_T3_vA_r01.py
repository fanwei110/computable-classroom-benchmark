import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率
position = 2_700_000       # 头寸金额（元）
confidence = 0.95          # 置信水平
trading_days = 252         # 一年交易日数假设

# 1. 将年化波动率换算为一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 计算95%置信水平下的正态分位数（损失侧，单尾）
z_score = -norm.ppf(1 - confidence)  # 结果为正值，如 1.64485

# 3. 计算一日 VaR（金额，正值表示损失）
var_95_1d = position * daily_vol * z_score

# 存入结果字典
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数，便于阅读
}

# 输出结果
print("计算结果：")
print(f"年化波动率: {annual_vol*100:.2f}%")
print(f"交易日数假设: {trading_days} 天/年")
print(f"一日波动率: {daily_vol*100:.4f}%")
print(f"95% 正态分位数 (Z): {z_score:.4f}")
print(f"头寸: {position:,.2f} 元")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print("\n最终结果字典：")
print(result)

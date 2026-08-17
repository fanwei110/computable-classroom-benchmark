import numpy as np
from scipy import stats

# 输入参数
value = 1_850_000  # 头寸价值（元）
annual_vol = 0.218  # 年化收益波动率
trading_days = 252  # 每年交易日

# 步骤1：计算一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 步骤2：获取单尾正态分位数
z_95 = stats.norm.ppf(0.95)  # 95%置信水平
z_99 = stats.norm.ppf(0.99)  # 99%置信水平

# 步骤3：计算VaR（均值取零）
# 95%一日VaR
var_95_1d = value * daily_vol * z_95

# 99%十日VaR（按sqrt(10)缩放）
var_99_10d = value * daily_vol * np.sqrt(10) * z_99

# 步骤4：结果字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 输出结果
print("参数法VaR计算结果：")
print(f"95%置信水平一日VaR: ¥{result['var_95_1d']:,.2f}")
print(f"99%置信水平十日VaR: ¥{result['var_99_10d']:,.2f}")
print("\n详细计算过程：")
print(f"一日波动率: {daily_vol:.6f} ({daily_vol*100:.4f}%)")
print(f"95%单尾分位数: {z_95:.4f}")
print(f"99%单尾分位数: {z_99:.4f}")
print(f"10日波动率缩放因子: √10 = {np.sqrt(10):.4f}")

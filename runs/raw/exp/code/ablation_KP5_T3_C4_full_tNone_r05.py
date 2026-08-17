import numpy as np
from scipy.stats import norm

# 给定参数
annual_vol = 0.24          # 年化波动率 24%
position = 2_700_000       # 头寸 2,700,000 元
confidence_level = 0.95    # 95% 置信水平
trading_days = 252         # 每年交易天数

# 1. 年化波动率去年化到一日
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 单尾 95% 正态分位数（均值取零）
z_score = norm.ppf(confidence_level)   # 约 1.64485

# 3. 计算 VaR（正的人民币金额）
var_95_1d = z_score * daily_vol * position

# 存入 result 字典
result = {
    'var_95_1d': var_95_1d
}

# 输出结果（便于课堂展示）
print(f"年化波动率: {annual_vol:.2%}")
print(f"一日波动率: {daily_vol:.6f}")
print(f"95% 单尾正态分位数: {z_score:.4f}")
print(f"头寸: {position:,.0f} 元")
print(f"一日 95% VaR: {var_95_1d:,.2f} 元")

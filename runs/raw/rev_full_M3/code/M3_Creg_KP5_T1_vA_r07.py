import numpy as np
from scipy.stats import norm

# --- 输入参数 ---
position_value = 1_850_000      # 头寸价值（元）
annual_vol = 0.218              # 年化收益波动率
trading_days_per_year = 252     # 假设一年的交易日数

# --- 模型计算 ---
# 1. 计算日波动率 (Delta-Normal模型下，波动率随时间的平方根缩放)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# 2. 计算10日波动率
vol_10d = annual_vol * np.sqrt(10 / trading_days_per_year)

# 3. 获取正态分布的分位数 (Z-score)
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# 4. 计算 VaR (VaR = 头寸价值 × Z分位数 × 波动率)
# (i) 95% 一日 VaR
var_95_1d = position_value * z_95 * daily_vol

# (ii) 99% 十日 VaR
var_99_10d = position_value * z_99 * vol_10d

# --- 输出契约 ---
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印结果以便验证
print(f"95% 一日 VaR: {result['var_95_1d']:.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:.2f} 元")

import numpy as np
from scipy.stats import norm

# ==================== 参数设置 ====================
position_value = 1_850_000.0   # 头寸价值（元）
annual_volatility = 0.218     # 年化收益波动率（21.8%）
trading_days_per_year = 252   # 每年交易日数

# ==================== 步骤 1: 去年化波动率 ====================
# 年化波动率缩放至一日：sigma_1d = sigma_annual / sqrt(252)
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# ==================== 步骤 2: 获取单尾正态分位数 ====================
# 短期限下均值取零，95%和99%的单尾分位数
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# ==================== 步骤 3: 计算 VaR ====================
# (i) 95% 一日 VaR = 头寸价值 × Z_95 × 一日波动率
var_95_1d = position_value * z_95 * daily_volatility

# (ii) 99% 十日 VaR = 头寸价值 × Z_99 × 一日波动率 × sqrt(10)
var_99_10d = position_value * z_99 * daily_volatility * np.sqrt(10)

# ==================== 步骤 4: 填充 result ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印结果以便投屏展示
print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")

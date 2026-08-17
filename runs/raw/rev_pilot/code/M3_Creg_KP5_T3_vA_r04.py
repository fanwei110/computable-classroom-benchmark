import numpy as np
from scipy.stats import norm

# --- 输入参数 ---
annual_volatility = 0.24  # 年化波动率 24%
position_value = 2700000  # 头寸规模 2,700,000 元
confidence_level = 0.95   # 95% 置信度
trading_days_per_year = 252  # 假设一年有252个交易日

# --- 计算过程 ---
# 1. 将年化波动率转换为日波动率
# 根据平方根时间法则: 日波动率 = 年化波动率 / sqrt(交易日数)
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 获取正态分布下 95% 置信度对应的分位数 (单尾)
z_score_95 = norm.ppf(confidence_level)

# 3. 计算 95% 一日 VaR
# VaR = 头寸价值 * 分位数 * 日波动率
var_95_1d = position_value * z_score_95 * daily_volatility

# --- 输出契约 ---
result = {
    'var_95_1d': var_95_1d
}

# 打印验证 (可选)
print(f"日波动率: {daily_volatility:.6f}")
print(f"95% 正态分位数: {z_score_95:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")

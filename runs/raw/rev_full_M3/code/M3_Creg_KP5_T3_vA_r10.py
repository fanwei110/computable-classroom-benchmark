import numpy as np
from scipy.stats import norm

# 已知参数
annual_vol = 0.24                 # 年化波动率 24%
position_value = 2700000          # 头寸 2,700,000 元
confidence_level = 0.95           # 95% 置信水平
trading_days_per_year = 252       # 金融市场常用的年均交易日数

# 计算一日波动率 (假设收益率服从正态分布，且各交易日独立同分布)
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# 获取 95% 置信水平下的正态分布分位数 (Z-score)
z_score = norm.ppf(confidence_level)

# 计算 95% 一日 VaR
# VaR = 头寸价值 * Z分位数 * 一日波动率
var_95_1d = position_value * z_score * daily_vol

# 按照输出契约存入字典
result = {
    'var_95_1d': var_95_1d
}

# 打印结果以供查看
print(f"一日波动率: {daily_vol:.6f}")
print(f"Z分位数 (95%): {z_score:.6f}")
print(f"95% 一日 VaR: {var_95_1d:.2f} 元")

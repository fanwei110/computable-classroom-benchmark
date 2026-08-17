import numpy as np
from scipy.stats import norm

# ==================== 参数设定 ====================
position_value = 1_850_000  # 仓位：185万人民币
vol_annual = 0.218          # 年化波动率：21.8%

# 假设：一年有252个交易日（金融计算中拆解日度数据的通用假设）
trading_days_per_year = 252

# ==================== 步骤1：换算一日期限波动率 ====================
# 参数法下，波动率与时间的平方根成正比：sigma_1d = sigma_annual / sqrt(T)
vol_1d = vol_annual / np.sqrt(trading_days_per_year)

# ==================== 步骤2：套用正态分位数 ====================
# 95% 和 99% 置信水平下的标准正态分布分位数（左尾取绝对值，即上侧分位数）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# ==================== 步骤3：计算VaR并缩放期限 ====================
# 计算 95% 1天 VaR (Delta-Normal 参数法公式：VaR = V * sigma * z)
var_95_1d = position_value * vol_1d * z_95

# 缩放到十日期限：sigma_10d = sigma_1d * sqrt(10)
vol_10d = vol_1d * np.sqrt(10)

# 计算 99% 10天 VaR
var_99_10d = position_value * vol_10d * z_99

# ==================== 步骤4：填充结果 ====================
# 以人民币报告，保留两位小数
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 课堂投屏输出辅助（便于学生直观理解）
print(f"--- 参数法 计算过程 ---")
print(f"年化波动率: {vol_annual:.2%}")
print(f"日度波动率: {vol_1d:.6%}")
print(f"10日波动率: {vol_10d:.6%}")
print(f"Z(95%): {z_95:.4f}  |  Z(99%): {z_99:.4f}")
print(f"-" * 25)
print(f"95% 1天 VaR: CNY {result['var_95_1d']:,.2f}")
print(f"99% 10天 VaR: CNY {result['var_99_10d']:,.2f}")

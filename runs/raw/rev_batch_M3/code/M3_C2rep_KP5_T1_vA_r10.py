import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
position_value = 1_850_000  # 头寸价值（人民币/元）
sigma_annual = 0.218        # 年化收益波动率

# ==================== 模型假设 ====================
# 假设一年有252个交易日，使用平方根法则进行期限调整
trading_days_per_year = 252

# ==================== 计算步骤 ====================

# 1. 把年化波动率换算到一日期限（日波动率）
# 根据Delta-Normal模型，日波动率 = 年化波动率 / sqrt(交易天数)
sigma_daily = sigma_annual / np.sqrt(trading_days_per_year)

# 2. 套用正态分位数（参数法核心假设：收益率服从正态分布）
z_95 = norm.ppf(0.95)  # 95%置信水平下的正态分布分位数
z_99 = norm.ppf(0.99)  # 99%置信水平下的正态分布分位数

# (i) 计算 95% 一日 VaR
var_95_1d = position_value * sigma_daily * z_95

# 3. 以合适方式缩放到十日期限并计算 99% 十日 VaR
# 十日波动率 = 一日波动率 * sqrt(10)
sigma_10d = sigma_daily * np.sqrt(10)

# (ii) 计算 99% 十日 VaR
var_99_10d = position_value * sigma_10d * z_99

# 4. 填充 result 字典（人民币金额保留2位小数符合财务习惯）
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# ==================== 输出验证 ====================
print(f"日波动率: {sigma_daily:.6f}")
print(f"十日波动率: {sigma_10d:.6f}")
print(f"95% 一日 VaR: {result['var_95_1d']} 元")
print(f"99% 十日 VaR: {result['var_99_10d']} 元")

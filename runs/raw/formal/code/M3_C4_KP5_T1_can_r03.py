import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
V = 1_850_000           # 头寸价值（人民币元）
sigma_annual = 0.218    # 年化收益波动率（小数表示）
trading_days = 252      # 每年交易日数

# ==================== 计算步骤 ====================
# 1. 去年化得到一日波动率
sigma_daily = sigma_annual / np.sqrt(trading_days)

# 2. 获取单尾正态分位数（均值取零）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# 3. 计算 95% 一日 VaR
var_95_1d = V * z_95 * sigma_daily

# 4. 计算 99% 十日 VaR，按 sqrt(10) 缩放
var_99_10d = V * z_99 * sigma_daily * np.sqrt(10)

# ==================== 结果封装 ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 输出结果以便教师投屏核对
print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")

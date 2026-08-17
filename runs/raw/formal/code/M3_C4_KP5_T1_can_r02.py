import numpy as np
from scipy.stats import norm

# ==================== 输入参数 ====================
V = 1_850_000.0      # 头寸价值（元）
sigma_ann = 0.218    # 年化收益波动率（小数表示）
trading_days = 252   # 每年交易日数

# ==================== 计算步骤 ====================

# 1. 去年化到一日：波动率按 sqrt(252) 缩放
sigma_1d = sigma_ann / np.sqrt(trading_days)

# 2. 提取单尾正态分位数（均值取零）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# 3. 计算 95% 一日 VaR
# VaR = 头寸价值 × 一日波动率 × 分位数
var_95_1d = V * sigma_1d * z_95

# 4. 计算 99% 十日 VaR
# 十日波动率按 sqrt(10) 缩放
sigma_10d = sigma_1d * np.sqrt(10)
var_99_10d = V * sigma_10d * z_99

# ==================== 输出结果 ====================
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 课堂投屏展示
print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")

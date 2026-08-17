import numpy as np
from scipy.stats import norm

# ==================== 初始参数设定 ====================
V = 1_850_000           # 头寸价值（元）
sigma_ann = 0.218       # 年化收益波动率
trading_days = 252      # 每年交易日数

# ==================== 计算步骤 ====================

# 1. 去年化波动率到一日（波动率按 sqrt(T) 缩放）
sigma_daily = sigma_ann / np.sqrt(trading_days)

# 2. 获取单尾正态分位数（短期限下均值取零）
z_95 = norm.ppf(0.95)
z_99 = norm.ppf(0.99)

# 3. 计算 VaR（报告为正的损失金额）
# (i) 95% 一日 VaR
var_95_1d = V * sigma_daily * z_95

# (ii) 99% 十日 VaR（十日波动率按 sqrt(10) 缩放）
sigma_10d = sigma_daily * np.sqrt(10)
var_99_10d = V * sigma_10d * z_99

# 4. 填充 result 字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# ==================== 课堂输出展示 ====================
print(f"每日波动率(去年化): {sigma_daily:.6f}")
print(f"10日波动率(缩放):   {sigma_10d:.6f}")
print("-" * 40)
print(f"95% 一日 VaR: {result['var_95_1d']:>12,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:>12,.2f} 元")

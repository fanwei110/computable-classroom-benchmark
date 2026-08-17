import numpy as np
from scipy.stats import norm

# ========== 给定参数 ==========
value = 1_850_000          # 头寸价值（元）
sigma_annual = 0.218       # 年化波动率
trading_days = 252         # 每年交易日

# ========== 去年化 ==========
sigma_daily = sigma_annual / np.sqrt(trading_days)

# ========== 单尾正态分位数（均值取零） ==========
z_95 = abs(norm.ppf(0.05))   # 95% 置信水平对应的临界值
z_99 = abs(norm.ppf(0.01))   # 99% 置信水平对应的临界值

# ========== VaR 计算 ==========
var_95_1d  = z_95 * sigma_daily * value                # 95% 一日 VaR
var_99_10d = z_99 * sigma_daily * np.sqrt(10) * value  # 99% 十日 VaR

# ========== 结果存入字典 ==========
result = {
    'var_95_1d':  var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印以便课堂投屏展示
print(result)

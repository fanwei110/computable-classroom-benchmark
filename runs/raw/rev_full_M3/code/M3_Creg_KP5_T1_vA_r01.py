import numpy as np
from scipy.stats import norm

# ---------------- 输入参数 ----------------
portfolio_value = 1_850_000      # 头寸价值 (元)
sigma_annual = 0.218             # 年化收益波动率
trading_days_per_year = 252      # 一年的交易日天数（金融计算标准惯例）

# ---------------- 波动率换算 ----------------
# 将年化波动率转换为日波动率
sigma_daily = sigma_annual / np.sqrt(trading_days_per_year)

# ---------------- 分位数计算 ----------------
# 95% 置信水平对应的单尾分位数
z_95 = norm.ppf(0.95)
# 99% 置信水平对应的单尾分位数
z_99 = norm.ppf(0.99)

# ---------------- VaR 计算 ----------------
# Delta-Normal 模型下：VaR = 头寸价值 × Z分位数 × 波动率
# (i) 95% 一日 VaR
var_95_1d = portfolio_value * z_95 * sigma_daily

# (ii) 99% 十日 VaR
# T日波动率 = 日波动率 × sqrt(T)
var_99_10d = portfolio_value * z_99 * sigma_daily * np.sqrt(10)

# ---------------- 结果输出 ----------------
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印结果以供验证
print(f"95% 一日 VaR: {result['var_95_1d']:.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:.2f} 元")

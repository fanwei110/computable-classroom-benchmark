import numpy as np
from scipy.stats import norm

# ---------------- 基本参数 ----------------
position_value = 1_850_000.0  # 头寸价值（元）
annual_vol = 0.218            # 年化收益波动率
trading_days_per_year = 252   # 惯例：一年252个交易日

# ---------------- 波动率换算 ----------------
# 将年化波动率转换为日波动率
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ---------------- 分位数计算 ----------------
# Delta-Normal模型下，使用标准正态分布的分位数
z_95 = norm.ppf(0.95)  # 95%置信度对应分位数
z_99 = norm.ppf(0.99)  # 99%置信度对应分位数

# ---------------- VaR 计算 ----------------
# (i) 95% 一日 VaR = 头寸价值 * Z_95 * 日波动率
var_95_1d = position_value * z_95 * daily_vol

# (ii) 99% 十日 VaR = 头寸价值 * Z_99 * (日波动率 * sqrt(10))
var_99_10d = position_value * z_99 * daily_vol * np.sqrt(10)

# ---------------- 输出契约 ----------------
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印结果以便验证（可选）
if __name__ == "__main__":
    print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
    print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")

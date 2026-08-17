import numpy as np
from scipy.stats import norm

# 输入参数
position_value = 1_850_000   # 头寸价值（元）
annual_vol = 0.218           # 年化收益波动率（小数形式）
trading_days = 252           # 每年交易日

# 单尾正态分位数
z_95 = norm.ppf(0.95)  # 约 1.64485
z_99 = norm.ppf(0.99)  # 约 2.32635

# 去年化到一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 计算一日 VaR (95%)
var_95_1d = position_value * daily_vol * z_95

# 十日波动率：一日波动率 * sqrt(10)
ten_day_vol = daily_vol * np.sqrt(10)
var_99_10d = position_value * ten_day_vol * z_99

# 输出字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

if __name__ == "__main__":
    print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
    print(f"99% 十日 VaR: {var_99_10d:,.2f} 元")

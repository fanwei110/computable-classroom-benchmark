import numpy as np
from scipy.stats import norm

# ---------- 输入参数 ----------
position_value = 1_850_000        # 头寸价值
annual_vol = 0.218                # 年化收益波动率
trading_days_per_year = 252       # 一年交易日数

# ---------- 正态分位数 ----------
z_95 = norm.ppf(0.95)             # 95% 单尾分位数
z_99 = norm.ppf(0.99)             # 99% 单尾分位数

# ---------- 波动率换算 ----------
vol_1d = annual_vol / np.sqrt(trading_days_per_year)          # 一日波动率
vol_10d = annual_vol * np.sqrt(10 / trading_days_per_year)    # 十日波动率

# ---------- VaR 计算（绝对值，表示损失）----------
var_95_1d = position_value * vol_1d * z_95
var_99_10d = position_value * vol_10d * z_99

# ---------- 按要求构建输出字典 ----------
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# ---------- 直接查看结果（可选）----------
if __name__ == '__main__':
    print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
    print(f"99% 十日 VaR: {var_99_10d:,.2f} 元")

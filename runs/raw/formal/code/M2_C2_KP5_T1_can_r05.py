import numpy as np
from scipy.stats import norm

# -------------------- 参数与假设 --------------------
position_value = 1_850_000   # 头寸价值（人民币元）
annual_vol = 0.218           # 年化收益波动率
trading_days = 252           # 假设一年有 252 个交易日（业界通用）

# 1. 年化波动率换算为一日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 标准正态分布下对应置信水平的分位数（左尾，负值）
z_95 = norm.ppf(0.05)   # 95% 置信水平对应的分位数
z_99 = norm.ppf(0.01)   # 99% 置信水平对应的分位数

# 3. 计算 VaR（假设收益均值为 0，VaR 取正数表示损失金额）
var_95_1d = position_value * daily_vol * abs(z_95)

# 十日波动率：波动率按时间平方根法则缩放
ten_day_vol = daily_vol * np.sqrt(10)
var_99_10d = position_value * ten_day_vol * abs(z_99)

# -------------------- 输出契约 --------------------
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

if __name__ == "__main__":
    print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
    print(f"99% 十日 VaR: {var_99_10d:,.2f} 元")
    print("\n结果字典:", result)

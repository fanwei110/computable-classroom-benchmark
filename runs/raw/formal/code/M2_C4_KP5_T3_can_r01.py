import numpy as np
from scipy.stats import norm

# 给定参数
annual_volatility = 0.24          # 年化波动率 24%
position_value = 2_700_000        # 头寸价值 2,700,000 元
trading_days_per_year = 252       # 每年交易日数
confidence_level = 0.95           # 置信水平 95%

# 步骤1：年化波动率去年化得到一日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 步骤2：单尾95%正态分位数（Z值，均值取零）
z_score = norm.ppf(confidence_level)

# 步骤3：计算一日 VaR（正损失金额）
var_95_1d = position_value * daily_volatility * z_score

# 输出契约
result = {
    'var_95_1d': var_95_1d
}

if __name__ == "__main__":
    print(f"一日波动率: {daily_volatility:.6f}")
    print(f"Z值 (单尾95%): {z_score:.6f}")
    print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
    print("结果字典:", result)

import numpy as np
from scipy.stats import norm

# 输入参数
annual_volatility = 0.24          # 年化波动率 24%
position_value = 2_700_000        # 头寸价值 2,700,000 元
confidence_level = 0.95           # 95%置信水平
trading_days = 252                # 年交易日数

# 步骤1: 年化波动率转为一日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days)

# 步骤2: 计算单尾95%正态分位数（均值取零）
z_score = norm.ppf(1 - confidence_level)  # ppf(0.05) 返回负数

# VaR计算：VaR = 头寸价值 × 日波动率 × |z_score|
# 注意：z_score为负值，取绝对值使VaR为正的损失金额
var_95_1d = position_value * daily_volatility * abs(z_score)

# 存储结果
result = {
    'var_95_1d': var_95_1d
}

# 输出结果
print(f"年化波动率: {annual_volatility*100:.1f}%")
print(f"一日波动率: {daily_volatility*100:.4f}%")
print(f"95%置信水平下的z值: {abs(z_score):.4f}")
print(f"95%一日VaR: ¥{var_95_1d:,.2f}")
print(f"\n结果字典: {result}")

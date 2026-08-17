import numpy as np
from scipy.stats import norm

# 假设一年有252个交易日
trading_days_per_year = 252

# 输入参数
annual_vol = 0.24  # 年化波动率 24%
position_value = 2_700_000  # 头寸 270万
confidence_level = 0.95  # 95% 置信水平

# 1. 年化波动率换算到一日期限
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# 2. 95% 正态分位数 (对于损失分位数，VaR取左侧尾部)
z_score = norm.ppf(1 - confidence_level)  # 95%置信水平对应标准正态分布的左尾分位数

# 3. 计算一日VaR金额
var_95_1d = position_value * daily_vol * abs(z_score)

# 输出结果
result = {
    'var_95_1d': var_95_1d
}

# 打印结果以便课堂投屏显示
print("=== 在险价值(VaR)计算结果 ===")
print(f"年化波动率: {annual_vol:.2%}")
print(f"头寸金额: ¥{position_value:,.0f}")
print(f"置信水平: {confidence_level:.0%}")
print(f"交易日假设: {trading_days_per_year}天/年")
print(f"日波动率: {daily_vol:.4%}")
print(f"正态分位数(Z-score): {z_score:.4f}")
print(f"95%一日VaR: ¥{var_95_1d:,.2f}")
print(f"\n结果字典: {result}")

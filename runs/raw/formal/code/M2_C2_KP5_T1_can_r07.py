import numpy as np
from scipy.stats import norm

# ============================
# 题目给定参数
# ============================
position_value = 1_850_000          # 头寸价值（元）
annual_vol = 0.218                 # 年化收益波动率
trading_days_per_year = 252        # 一年交易日数（标准假设）

# ============================
# 1. 将年化波动率换算为日波动率
# ============================
daily_vol = annual_vol / np.sqrt(trading_days_per_year)

# ============================
# 2. 计算两个置信水平下的正态分位数
#    delta-normal 模型假设零均值，VaR = 头寸价值 * 波动率 * z
#    其中 z = Φ^{-1}(置信水平)，损失取正数
# ============================
z_95 = norm.ppf(0.95)   # 95% 置信水平
z_99 = norm.ppf(0.99)   # 99% 置信水平

# ============================
# 3. 计算 VaR
# ============================
# (i) 95% 一日 VaR
var_95_1d = position_value * daily_vol * z_95

# (ii) 99% 十日 VaR —— 使用平方根法则缩放波动率
var_99_10d = position_value * daily_vol * np.sqrt(10) * z_99

# ============================
# 4. 将结果填入字典
# ============================
result = {
    'var_95_1d': var_95_1d,   # 95% 一日 VaR（元）
    'var_99_10d': var_99_10d, # 99% 十日 VaR（元）
}

# 输出查看（教师运行时可以直观看到）
print("Delta-Normal VaR 计算结果")
print("-" * 40)
print(f"头寸价值: {position_value:,.0f} 元")
print(f"年化波动率: {annual_vol*100:.2f}%")
print(f"假设年交易日: {trading_days_per_year} 天")
print(f"日波动率: {daily_vol*100:.4f}%")
print()
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print(f"99% 十日 VaR: {var_99_10d:,.2f} 元")

import numpy as np
from scipy.stats import norm

# 给定参数
position_value = 1_850_000   # 头寸价值（元）
annual_volatility = 0.218    # 年化收益波动率
trading_days = 252           # 一年交易日数目（标准假设）

# 1. 将年化波动率转换为日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days)

# 2. 正态分位数（Z值）
z_95 = norm.ppf(0.95)   # 95%置信水平对应的右尾分位数（正值）
z_99 = norm.ppf(0.99)   # 99%置信水平对应的右尾分位数（正值）

# 3. 计算一日 95% VaR
var_95_1d = position_value * daily_volatility * z_95

# 计算十日 99% VaR（使用平方根法则）
var_99_10d = position_value * daily_volatility * np.sqrt(10) * z_99

# 存入结果字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印输出（以便课堂演示）
print("=== Delta-Normal VaR 计算结果 ===")
print(f"头寸价值: {position_value:,.0f} 元")
print(f"年化波动率: {annual_volatility*100:.1f}%")
print(f"假设年交易日数: {trading_days}")
print(f"日波动率: {daily_volatility*100:.4f}%")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print(f"99% 十日 VaR: {var_99_10d:,.2f} 元")

# 如果需要单独查看字典
# print(result)

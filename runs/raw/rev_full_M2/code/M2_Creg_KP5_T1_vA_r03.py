import numpy as np
from scipy import stats

# 头寸价值
position_value = 1850000.0

# 年化收益波动率
annual_volatility = 0.218

# (i) 95% 一日 VaR
confidence_level_95 = 0.95
# 计算Z值（标准正态分布的分位数）
z_95 = stats.norm.ppf(1 - confidence_level_95)  # 95%置信水平对应的Z值
# 将年化波动率转换为日波动率（假设252个交易日）
daily_volatility = annual_volatility / np.sqrt(252)
# 一日VaR计算
var_95_1d = position_value * z_95 * daily_volatility

# (ii) 99% 十日 VaR
confidence_level_99 = 0.99
# 计算Z值
z_99 = stats.norm.ppf(1 - confidence_level_99)  # 99%置信水平对应的Z值
# 十日波动率（时间平方根法则）
ten_day_volatility = daily_volatility * np.sqrt(10)
# 十日VaR计算
var_99_10d = position_value * z_99 * ten_day_volatility

# 将所有结果存入字典
result = {
    'var_95_1d': var_95_1d,
    'var_99_10d': var_99_10d
}

# 打印结果以验证
print("Delta-Normal VaR计算结果:")
print(f"95% 一日 VaR: {var_95_1d:,.2f} 元")
print(f"99% 十日 VaR: {var_99_10d:,.2f} 元")

# 输出结果字典
print("\n结果字典:")
print(result)

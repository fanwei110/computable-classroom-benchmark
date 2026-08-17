import numpy as np
from scipy.stats import norm

# 给定数据
position_value = 1_850_000          # 头寸价值（人民币）
annual_volatility = 0.218           # 年化收益波动率
trading_days_per_year = 252         # 假设每年 252 个交易日

# 1. 年化波动率换算到一日波动率
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 计算正态分位数（左尾，损失对应负收益）
z_95 = norm.ppf(0.05)               # 95% 置信水平对应 5% 左尾分位
z_99 = norm.ppf(0.01)               # 99% 置信水平对应 1% 左尾分位

# 3. 一日 VaR（金额表示，取绝对值使输出为正数）
var_95_1d = abs(position_value * daily_volatility * z_95)

# 4. 十日 VaR：方差随时间累加，标准差按 sqrt(10) 缩放
var_99_10d = abs(position_value * daily_volatility * np.sqrt(10) * z_99)

# 5. 存入结果字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

# 输出结果（供课堂投屏展示）
print(f"头寸价值: {position_value:,.0f} 元")
print(f"年化波动率: {annual_volatility:.1%}")
print(f"交易日年化天数: {trading_days_per_year} 天")
print(f"一日波动率: {daily_volatility:.4%}\n")
print(f"95% 一日 VaR: {result['var_95_1d']:,.2f} 元")
print(f"99% 十日 VaR: {result['var_99_10d']:,.2f} 元")

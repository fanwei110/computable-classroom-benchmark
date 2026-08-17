import numpy as np
from scipy import stats
import json

# 参数设定
position_value = 2700000.0  # 头寸金额（元）
annual_volatility = 0.24    # 年化波动率 24%
confidence_level = 0.95     # 95% 置信水平
trading_days_per_year = 252 # 假设每年252个交易日

# 1. 将年化波动率换算到一日期限
# 假设收益率独立同分布，日波动率 = 年波动率 / sqrt(252)
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)
print(f"年化波动率: {annual_volatility:.2%}")
print(f"假设年交易日: {trading_days_per_year} 天")
print(f"一日波动率: {daily_volatility:.4%}")

# 2. 计算 95% 正态分位数
# 在险价值通常使用左尾分位数（损失为正）
# z_95 = norm.ppf(1 - 0.95) = norm.ppf(0.05)
z_score = stats.norm.ppf(1 - confidence_level)
print(f"95% 置信水平对应的正态分位数 (左尾): {z_score:.4f}")

# 3. 计算 VaR 金额
# VaR = 头寸 × 日波动率 × |z_score|
# 注：VaR 通常表示为正值（损失金额）
var_95_1d = position_value * daily_volatility * abs(z_score)
print(f"95% 一日 VaR 金额: {var_95_1d:,.2f} 元")

# 将结果存入字典
result = {
    'var_95_1d': var_95_1d
}

# 输出结果
print("\n=== 最终输出 ===")
print(json.dumps(result, indent=2, ensure_ascii=False))

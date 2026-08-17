import numpy as np
from scipy.stats import norm

# ========================
# 题目已知条件
# ========================
annual_volatility = 0.24          # 年化波动率 24%
position_value = 2_700_000.0      # 头寸价值 2,700,000 元
confidence_level = 0.95           # 95% 置信水平
trading_days_per_year = 252       # 交易日惯例（252天）

# ========================
# 1. 年化波动率转换为一日波动率
# ========================
# 假设收益率独立同分布，方差与时间成正比
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# ========================
# 2. 计算 95% 正态分布下的分位数（损失侧）
# ========================
# 损益分布：均值为0（假设预期收益为0，仅在短期VaR中常见且保守）
# norm.ppf(0.05) 给出标准正态分布的 5% 左尾分位数（负数）
z_score = norm.ppf(1 - confidence_level)  # 即 0.05 分位数，约为 -1.64485

# VaR 通常以正数表示潜在损失金额
var_95_1d = position_value * daily_volatility * abs(z_score)

# ========================
# 3. 存储结果
# ========================
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数，符合货币表示习惯
}

if __name__ == "__main__":
    print("计算完成，结果存入字典 result:")
    print(result)

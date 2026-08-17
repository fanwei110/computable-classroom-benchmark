import numpy as np
from scipy.stats import norm

# 给定参数
annual_volatility = 0.24          # 年化波动率
position_value = 2_700_000.0      # 头寸价值（元）
confidence_level = 0.95           # 置信水平
trading_days_per_year = 252       # 一年交易日假设

# 计算日波动率（假设无漂移，均值为0）
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 标准正态分布下95%置信水平对应的分位数（单尾）
z_score = norm.ppf(confidence_level)

# 1日VaR（绝对值，表示最大损失金额）
var_95_1d = position_value * daily_volatility * z_score

# 按输出契约存入字典
result = {
    'var_95_1d': var_95_1d
}

# 打印结果以验证
if __name__ == "__main__":
    print(result)

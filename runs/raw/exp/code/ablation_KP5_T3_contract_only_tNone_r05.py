import numpy as np
from scipy.stats import norm

# 已知参数
position = 2_700_000  # 头寸金额（元）
annual_volatility = 0.24  # 年化波动率 24%
confidence_level = 0.95  # 95%置信水平
days = 1  # 一天

# 年化波动率转换为日波动率 (假设252个交易日)
daily_volatility = annual_volatility / np.sqrt(252)

# 正态分布95%置信水平对应的单尾分位数 (左侧)
z_score = norm.ppf(1 - confidence_level)  # 对于损失侧为负值

# 计算VaR (损失金额为正数)
var_95_1d = -z_score * position * daily_volatility  # z_score为负，因此负负得正

# 输出结果字典
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数
}

print(f"95% 一日 VaR = {result['var_95_1d']} 元")

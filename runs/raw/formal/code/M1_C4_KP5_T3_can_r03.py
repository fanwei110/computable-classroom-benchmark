import numpy as np
from scipy.stats import norm

# 课程计算约定参数
TRADING_DAYS_PER_YEAR = 252
CONFIDENCE_LEVEL = 0.95
POSITION_VALUE = 2_700_000  # 头寸金额，单位：元
ANNUALIZED_VOLATILITY = 0.24  # 年化波动率，24%

# 1. 去年化一日波动率
daily_volatility = ANNUALIZED_VOLATILITY / np.sqrt(TRADING_DAYS_PER_YEAR)

# 2. 单尾 95% 正态分位数（均值为零）
z_score = norm.ppf(CONFIDENCE_LEVEL)

# 3. 计算一日 VaR（正的损失金额）
var_95_1d = POSITION_VALUE * z_score * daily_volatility

# 输出契约：存入 result 字典
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数，单位：元
}

# 打印结果以便课堂展示（可选）
print("95% 一日 VaR:", result['var_95_1d'], "元")

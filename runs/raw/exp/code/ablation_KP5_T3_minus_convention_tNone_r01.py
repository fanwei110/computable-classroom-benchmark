import numpy as np
from scipy.stats import norm

# 参数
position = 2_700_000          # 头寸，单位：元
annual_vol = 0.24             # 年化波动率 24%
days_per_year = 252           # 一年交易日数
confidence_level = 0.95       # 置信水平

# 步骤1：年化波动率换算为日波动率
daily_vol = annual_vol / np.sqrt(days_per_year)

# 步骤2：单尾95%的正态分位数（均值取0）
z_score = norm.ppf(confidence_level)   # 对于95%单尾，约1.64485

# 步骤3：计算 VaR（正的人民币金额）
var_95_1d = z_score * daily_vol * position

# 存入字典
result = {
    'var_95_1d': round(var_95_1d, 2)   # 保留两位小数，便于展示
}

# 输出结果
print(result)

import numpy as np
from scipy.stats import norm

# 输入参数
position = 2_700_000          # 头寸金额（元）
annual_vol = 0.24             # 年化波动率
confidence = 0.95             # 置信水平
trading_days = 252            # 一年交易天数（标准假设）

# 1. 年化波动率换算为日波动率
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. 95% 置信度下的正态分位数（单尾，取绝对值表示损失）
z_score = abs(norm.ppf(1 - confidence))

# 3. 计算一日 VaR（参数法，假设均值为零）
var_95_1d = position * daily_vol * z_score

# 4. 按要求存入 result 字典
result = {
    'var_95_1d': round(var_95_1d, 2)  # 保留两位小数，清晰展示
}

# 输出结果（供课堂投屏查看）
print(result)

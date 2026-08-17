import math
import scipy.stats as stats

# 给定参数
annual_vol = 0.24
position = 2_700_000
confidence = 0.95
trading_days = 252

# 日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 95% 置信水平对应的标准正态分位数（单尾）
z_score = stats.norm.ppf(confidence)

# 95% 单日 VaR（正数表示损失金额）
var_95_1d = position * daily_vol * z_score

# 结果字典
result = {
    'var_95_1d': round(var_95_1d, 2)
}

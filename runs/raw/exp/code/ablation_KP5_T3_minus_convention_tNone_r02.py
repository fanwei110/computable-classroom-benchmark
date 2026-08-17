import numpy as np
from scipy.stats import norm

# 参数
annual_volatility = 0.24          # 年化波动率 24%
position_value = 2_700_000       # 头寸 2,700,000 元
trading_days_per_year = 252      # 每年交易日数
confidence_level = 0.95          # 95% 置信水平

# 1. 年化波动率去年化到一日
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# 2. 单尾95%正态分位数（均值=0）
#    VaR对应的分位点是损失方向，即分布的左侧尾巴。
#    对于95%单尾，分位数 = norm.ppf(1 - 0.95) 等价于 norm.ppf(0.05)，是负值。
z_score = norm.ppf(1 - confidence_level)   # 例如 -1.64485...

# 3. 计算一日VaR（正的人民币金额）
#    VaR = - (均值0 + z_score * 日波动率 * 头寸金额) = - (z_score * daily_vol * position_value)
var_95_1d = -z_score * daily_volatility * position_value   # 因为z_score为负，取负后为正

# 4. 存入字典
result = {
    'var_95_1d': round(var_95_1d, 2)   # 保留两位小数，清晰显示金额
}

# 打印结果
print(result)

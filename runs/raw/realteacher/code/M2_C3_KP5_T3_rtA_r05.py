import math

def calculate_var():
    # 给定参数
    annual_vol = 0.24
    position = 2_700_000
    confidence = 0.95
    trading_days = 252

    # 日波动率
    daily_vol = annual_vol / math.sqrt(trading_days)

    # 95% 置信水平下的正态分布分位数（单尾）
    z_score = 1.6448536269514722  # norm.ppf(0.05) 的绝对值

    # 一日 VaR（正损失金额）
    var_95_1d = position * daily_vol * z_score

    result = {'var_95_1d': var_95_1d}
    return result

result = calculate_var()
result

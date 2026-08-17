import math

# 给定参数
position = 1_850_000      # 头寸金额
annual_vol = 0.218        # 年化波动率（小数）
trading_days = 252        # 每年交易日

# 置信水平对应的正态分布单尾分位数
z_95 = 1.6448536269514722   # 95% 置信水平
z_99 = 2.3263478740408408   # 99% 置信水平

# 计算一日 VaR (95%)
sigma_1d = annual_vol / math.sqrt(trading_days)
var_95_1d = position * sigma_1d * z_95

# 计算十日 VaR (99%)
sigma_10d = annual_vol * math.sqrt(10 / trading_days)
var_99_10d = position * sigma_10d * z_99

# 存入字典
result = {
    'var_95_1d': round(var_95_1d, 2),
    'var_99_10d': round(var_99_10d, 2)
}

result

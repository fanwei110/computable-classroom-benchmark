import math

# 给定参数
annual_vol = 0.24
position = 2_700_000
confidence = 0.95
trading_days = 252

# 计算日波动率
daily_vol = annual_vol / math.sqrt(trading_days)

# 正态分布95%分位数（单尾）
z_score = 1.6448536269514722  # 更精确的norm.ppf(0.95)

# 1日 VaR (正损失金额)
var_95_1d = position * z_score * daily_vol

result = {'var_95_1d': round(var_95_1d, 2)}
result

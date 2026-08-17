import math

# 已知参数
V = 2700000  # 270万元转为金额绝对值
sigma_annual = 0.24
trading_days = 252
z_95 = 1.6448536269514732  # norm.ppf(0.95)

# 计算日波动率
sigma_daily = sigma_annual / math.sqrt(trading_days)

# 计算 95% 一日 VaR（报告为正的损失金额）
var_95_1d = V * z_95 * sigma_daily

# 按输出契约存入字典
result = {
    'var_95_1d': var_95_1d
}

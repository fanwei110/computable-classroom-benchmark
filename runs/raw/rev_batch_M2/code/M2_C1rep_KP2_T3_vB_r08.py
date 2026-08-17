# 已知条件
beta = 1.42
market_return_monthly = -0.058  # 大盘上个月跌5.8%
rf_annual = 0.047               # 年化无风险利率4.7%

# 将年化无风险利率转换为月化（简单除以12）
rf_monthly = rf_annual / 12

# CAPM公式：E(R) = Rf + β * (Rm - Rf)
capm_return = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 存入结果字典
result = {
    'capm_return_monthly': round(capm_return, 6)  # 保留6位小数，约 -0.084005
}

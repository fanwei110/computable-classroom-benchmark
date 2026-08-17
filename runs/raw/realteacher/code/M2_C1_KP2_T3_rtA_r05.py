# 计算过程
beta = 1.42
market_return = -5.8  # 百分比
rf_annual = 4.7       # 年化百分比
rf_monthly = rf_annual / 12
expected_return = rf_monthly + beta * (market_return - rf_monthly)
result = {'capm_return_monthly': round(expected_return, 2)}

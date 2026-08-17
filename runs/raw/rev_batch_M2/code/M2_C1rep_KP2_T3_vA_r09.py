# 计算CAPM预期月收益
beta = 1.42
market_return_monthly = -0.058
rf_annual = 0.047
rf_monthly = rf_annual / 12

capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

result = {'capm_return_monthly': capm_return_monthly}

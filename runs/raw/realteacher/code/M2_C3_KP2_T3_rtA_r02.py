import numpy as np

beta = 1.42
market_return_monthly = -0.058
rf_annual = 0.047
trading_days = 252
monthly_days = 21

rf_monthly = (1 + rf_annual) ** (monthly_days / trading_days) - 1

capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

result = {'capm_return_monthly': capm_return_monthly}

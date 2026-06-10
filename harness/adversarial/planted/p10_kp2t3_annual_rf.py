# PLANTED ERROR (T3, conventional): plugs the ANNUAL risk-free rate into a
# MONTHLY CAPM equation without converting it. Not an enumerated defensible
# convention. Expected: numeric_wrong, tier wrong.
beta = 1.42
market_monthly = -0.058
rf = 0.047

result = {"capm_return_monthly": rf + beta * (market_monthly - rf)}

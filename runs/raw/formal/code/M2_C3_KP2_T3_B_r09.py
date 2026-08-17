# è®¡ç®è¿ç¨
annual_rf = 0.047
monthly_rf = (1 + annual_rf) ** (1/12) - 1
beta = 1.42
market_return = -0.058

capm_return = monthly_rf + beta * (market_return - monthly_rf)

result = {'capm_return_monthly': capm_return}

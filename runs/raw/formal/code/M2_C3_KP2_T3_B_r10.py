# è®¡ç®è¿ç¨
rf_annual = 0.047
rf_monthly = (1 + rf_annual) ** (21/252) - 1
beta = 1.42
rm = -0.058
capm_return_monthly = rf_monthly + beta * (rm - rf_monthly)

result = {'capm_return_monthly': capm_return_monthly}
# ç»æçº¦ä¸º -0.08397

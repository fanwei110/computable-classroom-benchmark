# è®¡ç®è¿ç¨
rf_annual = 0.047
beta = 1.42
market_monthly = -0.058

# å¹´åæ é£é©å©çè½¬æåº¦ï¼æ252ä¸ªäº¤ææ¥ï¼ä¸ä¸ªæå21ä¸ªäº¤ææ¥ï¼
rf_monthly = (1 + rf_annual) ** (21/252) - 1

# CAPMé¢ææ¶ç
capm_return_monthly = rf_monthly + beta * (market_monthly - rf_monthly)

result = {'capm_return_monthly': capm_return_monthly}

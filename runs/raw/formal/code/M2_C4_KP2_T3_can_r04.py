import numpy as np

# ç»å®æ°æ®
beta = 1.42
market_return_monthly = -0.058   # å¸åºä¸æä¸è· 5.8%
rf_annual = 0.047                # å¹´æ é£é©å©ç 4.7%

# 1. å¹´å©çç®åæç®ä¸ºæå©ç
rf_monthly = rf_annual / 12.0

# 2. æåº¦å±é¢ CAPM å: E(R) = Rf + beta * (Rm - Rf)
capm_return_monthly = rf_monthly + beta * (market_return_monthly - rf_monthly)

# 3. æè¦æ±å­åå­å
result = {
    'capm_return_monthly': capm_return_monthly
}

print(result)

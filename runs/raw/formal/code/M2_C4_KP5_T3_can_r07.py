import numpy as np
from scipy.stats import norm

# ç»å®åæ°
annual_vol = 0.24            # å¹´åæ³¢å¨ç
position_value = 2_700_000   # å¤´å¯¸éé¢ï¼åï¼
confidence_level = 0.95      # åå°¾ç½®ä¿¡æ°´å¹³
trading_days = 252           # å¹´äº¤ææ¥æ°

# 1. å»å¹´åå¾å°ä¸æ¥æ³¢å¨ç
daily_vol = annual_vol / np.sqrt(trading_days)

# 2. åå°¾95%æ­£æåä½æ°ï¼åå¼åé¶ï¼
z_score = norm.ppf(confidence_level)

# 3. è®¡ç®VaRï¼æ­£æå¤±éé¢ï¼
var_95_1d = position_value * daily_vol * z_score

# è¾åºå¥çº¦
result = {
    'var_95_1d': round(var_95_1d, 2)
}

# å¯éæå°ï¼æ¹ä¾¿æå±å±ç¤º
print(result)

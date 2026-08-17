import math
from scipy.stats import norm

# è¾åæ°æ®
annual_vol = 0.24
position = 2_700_000
trading_days = 252
confidence_level = 0.95

# è®¡ç®ä¸æ¥æ³¢å¨ç
daily_vol = annual_vol / math.sqrt(trading_days)

# è®¡ç®95%ç½®ä¿¡åº¦å¯¹åºçæ­£æåå¸åä½æ°ï¼åå°¾ï¼
z_score = norm.ppf(confidence_level)

# è®¡ç®ä¸æ¥VaRï¼æ¥åä¸ºæ­£çæå¤±éé¢ï¼
var_95_1d = position * daily_vol * z_score

result = {
    'var_95_1d': round(var_95_1d, 2)
}

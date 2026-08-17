import numpy as np

def compute_price_drop():
    """
    è®¡ç®åºå¸ä»·æ ¼å¨æ¶ççä¸å80ä¸ªåºç¹æ¶çè·å¹ï¼ä¸é¶ä¿®æ­£ä¹æè¿ä¼¼ï¼ã
    
    åºå¸åæ°ï¼
    - é¢å¼: 100
    - ç¥¨æ¯ç: 4.6% (å¹´ä»æ¯)
    - å°æå¹´é: 7
    - å½åæ¶çç: 5.3% (å¹´å¤å©)
    - æ¶ççåå¨: +80 åºç¹ = 0.008
    """
    face = 100.0
    coupon_rate = 0.046
    y = 0.053
    maturity = 7
    dy = 0.008  # 80 bps

    # ç°éæµæ¶é´ç¹ (å¹´æ«)
    t = np.arange(1, maturity + 1, dtype=float)

    # æ¯æç°éæµ: å6å¹´ç¥¨æ¯ï¼æåä¸å¹´ç¥¨æ¯+é¢å¼
    cf = np.full(maturity, coupon_rate * face)
    cf[-1] += face

    # æç°å å­ä¸ç°å¼
    discount = (1 + y) ** t
    pv = cf / discount

    # åºå¸ä»·æ ¼
    P = np.sum(pv)

    # éº¦èå©ä¹æ
    D_mac = np.sum(t * pv) / P

    # ä¿®æ­£ä¹æ (å¹´å¤å©)
    D_mod = D_mac / (1 + y)

    # ä¸é¶è¿ä¼¼: dP/P â -D_mod * dy
    # é¢ç®è¦æ±è·å¹ä¸ºæ­£çå°æ°ï¼æåç»å¯¹å¼
    price_drop_pct = D_mod * dy

    return price_drop_pct


price_drop = compute_price_drop()

# æè¦æ±ç»ç»è¾åº
result = {'price_drop_pct': price_drop}

print(result)

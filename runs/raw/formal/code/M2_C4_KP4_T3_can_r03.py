import numpy as np
from scipy.stats import norm

def bs_call_price(S, K, T, r, sigma):
    """
    Black-Scholes æ¬§å¼çæ¶¨ææå®ä»·åï¼è¿ç»­å¤å©ï¼
    S: æ çç°ä»·
    K: è¡æä»·
    T: å©ä½æéï¼å¹´ï¼
    r: æ é£é©å©çï¼å°æ°ï¼
    sigma: æ³¢å¨çï¼å°æ°ï¼
    """
    if T <= 0:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price

# ç»å®åæ°
S = 103.7
K = 97.5
T = 0.58
r = 0.043
sigma_base = 0.276
sigma_up = 0.286

# ç²¾ç¡®éå®ä»·
price_base = bs_call_price(S, K, T, r, sigma_base)
price_up = bs_call_price(S, K, T, r, sigma_up)

# ä»·å·®
price_change = price_up - price_base

# æè¦æ±å­å¨ç»æ
result = {'price_change': price_change}

# è¾åºç»æä»¥ä¾¿è¯¾å æå±æ¥ç
print("Black-Scholes çæ¶¨ææå®ä»·")
print(f"åæ°: S={S}, K={K}, T={T}, r={r}")
print(f"æ³¢å¨ç {sigma_base:.1%} æ¶ä»·æ ¼: {price_base:.6f}")
print(f"æ³¢å¨ç {sigma_up:.1%} æ¶ä»·æ ¼: {price_up:.6f}")
print(f"éå«æ³¢å¨çä¸åä¸ä¸ªç¾åç¹çä»·æ ¼åå¨: {price_change:.6f}")
print("\nç»æå­å:")
print(result)

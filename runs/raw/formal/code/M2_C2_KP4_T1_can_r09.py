import numpy as np
from scipy.stats import norm

def main():
    # ----- ç»å®åæ° -----
    S     = 103.7      # æ çç°ä»·
    K     = 97.5       # è¡æä»·
    sigma = 0.276      # å¹´åéå«æ³¢å¨ç (27.6%)
    r     = 0.043      # å¹´åæ é£é©å©ç (4.3%)
    T     = 0.58       # å©ä½æé (å¹´)

    # ----- 1. è®¡ç® d1 ä¸ d2 -----
    sqrt_T = np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T

    # ----- 2. è®¡ç®ææä»·æ ¼ä¸ delta -----
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    call_delta = norm.cdf(d1)           # çæ¶¨ delta = N(d1)

    # ----- 3. è®¡ç® vegaï¼ä»·æ ¼å¯¹æ³¢å¨ççåå¯¼æ°ï¼-----
    call_vega = S * norm.pdf(d1) * sqrt_T   # âC/âÏ

    # ----- 4. å¡«åå¥çº¦å­å -----
    result = {
        'call_price': call_price,
        'call_delta': call_delta,
        'call_vega': call_vega
    }

    # è¾åºå°æ§å¶å°ï¼æ¹ä¾¿è¯¾ä¸æå±æ¥ç
    for k, v in result.items():
        print(f"{k}: {v:.6f}")

    # ä¿ç result åéä¾å¯è½çåç»­ä½¿ç¨
    return result

if __name__ == "__main__":
    result = main()

import numpy as np

def main():
    # ç»å®çå¹´åæ³¢å¨ç
    sigma = np.array([0.187, 0.243, 0.312])
    # ç»å®çç¸åæ°ç©éµ (ä¸ä¸è§å·²å¯¹ç§°ï¼è¿éååºå®æ´ç©éµ)
    corr = np.array([
        [ 1.00,  0.21, -0.13],
        [ 0.21,  1.00,  0.37],
        [-0.13,  0.37,  1.00]
    ])
    
    # 1. æé åæ¹å·®ç©éµï¼cov(i,j) = corr(i,j) * sigma_i * sigma_j
    # ä½¿ç¨å¤ç§¯è®¡ç®æ åå·®ä¹ç§¯ç©éµï¼åä¸ç¸åæ°ç©éµéåç¸ä¹
    cov = corr * np.outer(sigma, sigma)
    
    # 2. è®¡ç®åæå°æ¹å·®ç»åæéï¼ååç©ºï¼æ»¡ä»çº¦æ w'1 = 1ï¼
    # é­å¼è§£: w = (Î£^{-1} 1) / (1' Î£^{-1} 1)
    inv_cov = np.linalg.inv(cov)
    ones = np.ones(3)
    # åå­: Î£^{-1} 1
    numerator = inv_cov @ ones
    # åæ¯: 1' Î£^{-1} 1 (æ é)
    denominator = ones @ numerator
    # åæå°æ¹å·®æé
    w_mvp = numerator / denominator
    
    # 3. è®¡ç®ç»åå¹´åæ³¢å¨çï¼sqrt(w' Î£ w)
    var_mvp = w_mvp @ cov @ w_mvp
    vol_mvp = np.sqrt(var_mvp)
    
    # 4. æé è¾åºå­åï¼é®åä¸¥æ ¼æé¢ç®è¦æ±
    result = {
        'mvp_weights': w_mvp.tolist(),  # è½¬ä¸ºåè¡¨ä¾¿äºæ¥ç
        'mvp_vol_annual': float(vol_mvp)  # ç¡®ä¿ä¸ºPythonåçæµ®ç¹æ°
    }
    
    # è¾åºç»æï¼å±å¹ä¸å°æ¾ç¤ºå­ååï¼
    print("åæå°æ¹å·®ç»åç»æï¼")
    print(f"æé: {w_mvp}")
    print(f"å¹´åæ³¢å¨ç: {vol_mvp:.6f}")
    print("\nè¾åºå­å result:")
    print(result)

if __name__ == "__main__":
    main()

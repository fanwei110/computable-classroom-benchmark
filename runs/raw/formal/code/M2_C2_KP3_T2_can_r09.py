import numpy as np
import matplotlib.pyplot as plt

# ========================================================
# åºå¸åæ°è®¾å®ï¼å¯è°é¨åï¼
# ========================================================
FACE_VALUE = 100.0         # é¢å¼
COUPON_RATE = 0.046        # ç¥¨æ¯çï¼å¹´åï¼
MATURITY = 7               # å©ä½æéï¼å¹´ï¼
Y0 = 0.053                 # å½åå°ææ¶çç
SHIFT_BP = 100             # æ¶ççåå¨å¹ï¼åºç¹ï¼ï¼å¯è°
DY = SHIFT_BP / 10000      # åä¸ºå°æ°å½¢å¼ï¼100 bp = 1%ï¼

# åè®¾å¹´ä»æ¯ä¸æ¬¡ï¼è¿æ¯å½åææå¸¸è§åè®¾ï¼ä¸ä¸ä¹æä¿®æ­£åä¿æä¸è´
COUPON = FACE_VALUE * COUPON_RATE

# ç°éæµæ¶é´ç¹ï¼ç¬¬1,2,...,7å¹´æ«ï¼
T = np.arange(1, MATURITY + 1)
# åæç°éæµï¼å6æåä¸ºç¥¨æ¯ï¼æåä¸æä¸ºç¥¨æ¯+é¢å¼
CF = np.full(MATURITY, COUPON)
CF[-1] += FACE_VALUE


# ========================================================
# å®ä»·å½æ°ï¼å¹´å¤å©è´´ç°ï¼
# ========================================================
def bond_price_scalar(ytm):
    """è®¡ç®ç»å®å°ææ¶ççytmä¸çåºå¸ä»·æ ¼ï¼æ éçæ¬ï¼"""
    pv = CF / (1 + ytm) ** T
    return np.sum(pv)


def bond_price_array(ytm_array):
    """è®¡ç®ç»å®å°ææ¶ççæ°ç»ä¸çåºå¸ä»·æ ¼ï¼åéåçæ¬ï¼"""
    # å°ç°éæµè´´ç°å å­å¨æ¶é´è½´ä¸å¹¿æ­
    discount = (1 + ytm_array[np.newaxis, :]) ** (-T[:, np.newaxis])
    pv = CF[:, np.newaxis] * discount
    return np.sum(pv, axis=0)


# ========================================================
# 1. ç²¾ç¡®ä»·æ ¼-æ¶ççæ²çº¿
# ========================================================
Y_GRID = np.linspace(0.02, 0.09, 500)   # æ¶ççèå´ 2% ~ 9%
P_EXACT = bond_price_array(Y_GRID)      # ç²¾ç¡®ä»·æ ¼

# å½åæ¶ççä¸çä»·æ ¼
P0 = bond_price_scalar(Y0)

# ========================================================
# 2. ä¹æè®¡ç®ï¼éº¦èå©ä¹æ â ä¿®æ­£ä¹æï¼
# ========================================================
PV0 = CF / (1 + Y0) ** T
D_MAC = np.sum(T * PV0) / P0                 # éº¦èå©ä¹æ
D_MOD = D_MAC / (1 + Y0)                     # ä¿®æ­£ä¹æï¼å¹´å¤å©ï¼

# åºäºä¹æçè¿ä¼¼ä»·æ ¼ï¼P_approx(y) = P0 - P0 * D_mod * (y - y0)
P_APPROX = P0 - P0 * D_MOD * (Y_GRID - Y0)

# ========================================================
# 3. æ¶ççä¸å100bp åçè¡¨ç°
# ========================================================
Y_UP = Y0 + DY                               # ä¸ååçæ¶çç
P_UP_EXACT = bond_price_scalar(Y_UP)         # ç²¾ç¡®ä»·æ ¼

# ç²¾ç¡®ç¸å¯¹ä»·æ ¼åå
exact_relative_change = (P_UP_EXACT - P0) / P0

# ä¹ææ³ä¼°è®¡çç¸å¯¹ä»·æ ¼åå
dur_approx_change = -D_MOD * DY

# ========================================================
# 4. ç»å¾å¹¶ä¿å­å¾å½¢
# ========================================================
plt.figure(figsize=(10, 6))
plt.plot(Y_GRID, P_EXACT, label='Exact Price-Yield Curve', linewidth=2)
plt.plot(Y_GRID, P_APPROX, '--', label='Duration-based Approximation',
         linewidth=2, color='darkorange')
plt.axvline(Y0, color='grey', linestyle=':', alpha=0.6, label=f'Current YTM={Y0:.2%}')
plt.axvline(Y_UP, color='red', linestyle=':', alpha=0.6,
            label=f'Shifted YTM (+{SHIFT_BP}bp) = {Y_UP:.2%}')
plt.xlabel('Yield to Maturity')
plt.ylabel('Bond Price')
plt.title('Bond Price-Yield Curve: Exact vs. Duration Approximation')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

FIGURE_PATH = 'bond_price_yield_curve.png'
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()   # éæ¾åï¼é¿åå¨éäº¤äºç¯å¢ä¸­æ¾ç¤º

# ========================================================
# 5. ç»ç»è¾åºç»æ
# ========================================================
result = {
    'price_at_up100bp': P_UP_EXACT,               # æ¶ççä¸å100bpåçç²¾ç¡®ä»·æ ¼
    'dur_approx_change_up100bp': dur_approx_change, # ä¹ææ³ä¼°è®¡çç¸å¯¹ä»·æ ¼ååï¼å°æ°å½¢å¼ï¼
    'figure_path': FIGURE_PATH                     # å¾å½¢ä¿å­è·¯å¾
}

# æå°ç»ææ¹ä¾¿æå¸æ¥ç
print("========== åºå¸å®ä»·ä¸ä¹æåæç»æ ==========")
print(f"å½åæ¶çç (Y0): {Y0:.2%}")
print(f"å½åä»·æ ¼ (P0): {P0:.4f}")
print(f"ä¿®æ­£ä¹æ (D_mod): {D_MOD:.4f} å¹´")
print(f"æ¶ççä¸å {SHIFT_BP} bp åçç²¾ç¡®ä»·æ ¼: {P_UP_EXACT:.4f}")
print(f"ç²¾ç¡®ç¸å¯¹ä»·æ ¼åå: {exact_relative_change:.6f} ({exact_relative_change:.4%})")
print(f"ä¹ææ³ä¼°è®¡çç¸å¯¹ä»·æ ¼åå: {dur_approx_change:.6f} ({dur_approx_change:.4%})")
print(f"å¾è¡¨ä¿å­è·¯å¾: {FIGURE_PATH}")
print("\nç»æå­å result:")
print(result)

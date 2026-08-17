import numpy as np
import matplotlib.pyplot as plt

# ---------- åºå¸åæ° ----------
face_value = 100
coupon_rate = 0.046
coupon = face_value * coupon_rate
maturity = 7
y0 = 0.053  # åå§æ¶çç

# ---------- è¾å½æ° ----------
def bond_price(y):
    """è®¡ç®åºå¸ä»·æ ¼ï¼æ¯å¹´ä»æ¯ä¸æ¬¡ï¼"""
    t = np.arange(1, maturity + 1)
    pv_coupons = coupon / (1 + y) ** t
    pv_face = face_value / (1 + y) ** maturity
    return np.sum(pv_coupons) + pv_face

def macaulay_duration(y):
    """éº¦èå©ä¹æ"""
    t = np.arange(1, maturity + 1)
    pv_cf = coupon / (1 + y) ** t
    pv_face = face_value / (1 + y) ** maturity
    p = np.sum(pv_cf) + pv_face
    weighted_sum = np.sum(t * pv_cf) + maturity * pv_face
    return weighted_sum / p

# ---------- ç²¾ç¡®è®¡ç® ----------
P0 = bond_price(y0)
D_mac = macaulay_duration(y0)
D_mod = D_mac / (1 + y0)

# æ¶ççä¸å100ä¸ªåºç¹
dy = 0.01
y_up = y0 + dy
P_up_exact = bond_price(y_up)

# ç¸å¯¹ä»·æ ¼ååï¼ç²¾ç¡®ï¼
exact_change = (P_up_exact - P0) / P0

# ä¹æä¼°è®¡çç¸å¯¹ä»·æ ¼åå
dur_approx_change = -D_mod * dy

# ---------- ç»å¾ ----------
# æ¶ççèå´
y_range = np.linspace(0.02, 0.09, 200)
prices_exact = [bond_price(y) for y in y_range]

# å¯è°çæ¶ççåå¨å¹ï¼ç¨åéæ§å¶åçº¿æ¾ç¤ºèå´ï¼é»è®¤å±ç¤º Â±300bpï¼
# æ¨å¯ä»¥ä¿®æ¹è¿ä¸ªå¼æ¥è°æ´è¿ä¼¼çº¿å¨å¾ä¸­å»¶ä¼¸çå®½åº¦
y_shift_span = 0.03  # å½åæ¶ççä¸¤ä¾§åæ©å± 300bp å±ç¤ºåçº¿

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_range * 100, prices_exact, label='ç²¾ç¡®ä»·æ ¼æ²çº¿', linewidth=2)

# ä¹æè¿ä¼¼ï¼åçº¿ P(y) â P0 * (1 - D_mod * (y - y0))
y_tangent = np.linspace(y0 - y_shift_span, y0 + y_shift_span, 50)
p_tangent = P0 * (1 - D_mod * (y_tangent - y0))
ax.plot(y_tangent * 100, p_tangent, '--', label='ä¹æè¿ä¼¼ (åçº¿)', linewidth=2)

# æ æ³¨å½åç¹
ax.plot(y0 * 100, P0, 'ro', label=f'å½å (y={y0*100:.1f}%)')
ax.set_xlabel('æ¶çç (%)')
ax.set_ylabel('åºå¸ä»·æ ¼')
ax.set_title('åºå¸ä»·æ ¼éæ¶ççåååä¹æè¿ä¼¼')
ax.legend()
ax.grid(True)

# ä¿å­å¾ç
figure_path = 'bond_price_duration.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ---------- ç»æå­åå­å ----------
result = {
    'price_at_up100bp': round(P_up_exact, 4),          # æ¶ççä¸å100bpåçç²¾ç¡®ä»·æ ¼
    'dur_approx_change_up100bp': round(dur_approx_change, 6),  # ä¹æä¼°è®¡çç¸å¯¹ä»·æ ¼ååï¼å°æ°å½¢å¼ï¼
    'figure_path': figure_path
}

print(result)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- åºå¸åæ° ----------
face = 100.0
coupon_rate = 0.046   # 4.6%
years = 7
freq = 1             # å¹´ä»æ¯
y0 = 0.053           # å½åæ¶çç
shift_bp = 100       # æ¶ççåå¨å¹ï¼å¯è°åæ°ï¼
dy = shift_bp / 10000  # è½¬æ¢æå°æ°ï¼100 bp = 0.01

# ---------- ç²¾ç¡®ä»·æ ¼å½æ° ----------
def bond_price(ytm):
    """å¹´å¤å©åºå¸ä»·æ ¼"""
    t = np.arange(1, years + 1)
    cf = np.full(years, face * coupon_rate)
    cf[-1] += face
    pv = np.sum(cf / (1 + ytm) ** t)
    return pv

P0 = bond_price(y0)
P_up = bond_price(y0 + dy)

# ---------- éº¦èå©ä¹æ & ä¿®æ­£ä¹æ ----------
t = np.arange(1, years + 1)
cf = np.full(years, face * coupon_rate)
cf[-1] += face
pv_cf = cf / (1 + y0) ** t
mac_dur = np.sum(t * pv_cf) / P0
mod_dur = mac_dur / (1 + y0)
approx_rel_change = -mod_dur * dy          # ä¹æä¼°è®¡çç¸å¯¹ä»·æ ¼åå

# ---------- ç»å¾ ----------
y_range = np.linspace(0.02, 0.09, 200)
price_exact = [bond_price(y) for y in y_range]

# åçº¿ï¼P(y) â P0 - P0 * mod_dur * (y - y0)
price_approx = P0 - P0 * mod_dur * (y_range - y0)

plt.figure(figsize=(10, 6))
plt.plot(y_range * 100, price_exact, label='ç²¾ç¡®ä»·æ ¼ (Full Pricing)', linewidth=2)
plt.plot(y_range * 100, price_approx, '--', label='ä¹æè¿ä¼¼ (Duration Approximation)', linewidth=2)

# æ è®°å½åæ¶ççç¹
plt.axvline(y0 * 100, color='gray', linestyle=':', alpha=0.7)
plt.scatter([y0 * 100], [P0], color='black', zorder=5)
plt.text(y0 * 100 + 0.1, P0, f'å½å YTM={y0*100:.2f}%', fontsize=9)

# æ è®°æ¶ççä¸å 100 bp çç¹
y_up = y0 + dy
P_up_approx = P0 - P0 * mod_dur * dy
plt.scatter([y_up * 100], [P_up], color='red', zorder=5, label=f'ç²¾ç¡®ä»·æ ¼ @ +{shift_bp}bp')
plt.scatter([y_up * 100], [P_up_approx], color='orange', marker='s', zorder=5, label=f'è¿ä¼¼ä»·æ ¼ @ +{shift_bp}bp')
plt.plot([y_up * 100, y_up * 100], [P_up, P_up_approx], color='red', linestyle=':', alpha=0.6)

# å¯è°å¹è¯´æ
plt.text(0.05, 0.95, f'æ¶ççåå¨å¹ Îy = {shift_bp} bpï¼å¯è°ï¼', transform=plt.gca().transAxes,
         fontsize=11, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.xlabel('æ¶çç (%)')
plt.ylabel('ä»·æ ¼')
plt.title('åºå¸ä»·æ ¼-æ¶ççæ²çº¿ & ä¹æè¿ä¼¼')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

fig_path = 'price_yield_curve.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# ---------- ç»ææ±æ» ----------
result = {
    'price_at_up100bp': round(P_up, 4),
    'dur_approx_change_up100bp': round(approx_rel_change, 4),
    'figure_path': fig_path
}

print(result)

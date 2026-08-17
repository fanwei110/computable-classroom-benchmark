import numpy as np
import matplotlib.pyplot as plt

# ---------- åºå¸åæ° ----------
face = 100.0
coupon = 4.6
T = 7
ytm = 0.053
dy = 0.01          # åå¨å¹ï¼å¯è°
y_min, y_max = 0.02, 0.09

# ---------- ä»·æ ¼è®¡ç®å½æ°ï¼å¹´å¤å©ï¼ ----------
def bond_price(y, c, f, t):
    pv = sum(c / (1+y)**i for i in range(1, t+1))
    pv += f / (1+y)**t
    return pv

P0 = bond_price(ytm, coupon, face, T)

# ---------- ä¿®æ­£ä¹æ ----------
pvs = [coupon / (1+ytm)**i for i in range(1, T+1)]
pvs.append(face / (1+ytm)**T)
weights = [pv / P0 for pv in pvs]
times = list(range(1, T+1)) + [T]
mac_dur = sum(t * w for t, w in zip(times, weights))
mod_dur = mac_dur / (1+ytm)

# ---------- ç²¾ç¡®ä»·æ ¼ï¼+100bpï¼ ----------
price_up = bond_price(ytm + dy, coupon, face, T)

# ---------- ä¹æè¿ä¼¼ç¸å¯¹åå ----------
dur_approx_change = -mod_dur * dy

# ---------- ç»å¾ ----------
y_vals = np.linspace(y_min, y_max, 200)
price_exact = [bond_price(y, coupon, face, T) for y in y_vals]
price_approx = P0 - P0 * mod_dur * (y_vals - ytm)

plt.figure(figsize=(10,6))
plt.plot(y_vals, price_exact, label='ç²¾ç¡®ä»·æ ¼', linewidth=2)
plt.plot(y_vals, price_approx, '--', label='ä¹æè¿ä¼¼ï¼åçº¿ï¼', linewidth=2)
plt.axvline(ytm, color='gray', linestyle=':', alpha=0.7)
plt.axvline(ytm+dy, color='gray', linestyle=':', alpha=0.7)
plt.scatter([ytm], [P0], color='black', zorder=5)
plt.scatter([ytm+dy], [price_up], color='red', zorder=5, label=f'æ¶çç+100bpç²¾ç¡®ä»·æ ¼: {price_up:.4f}')
plt.xlabel('æ¶ççï¼å¹´å¤å©ï¼')
plt.ylabel('ä»·æ ¼')
plt.title('åºå¸ä»·æ ¼âæ¶ççæ²çº¿')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

fig_path = 'bond_price_duration.png'
plt.savefig(fig_path)
plt.close()

# ---------- è¾åºå­å ----------
result = {
    'price_at_up100bp': round(price_up, 4),
    'dur_approx_change_up100bp': round(dur_approx_change, 6),
    'figure_path': fig_path
}

result

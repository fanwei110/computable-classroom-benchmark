import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# =========================
# å¯è°åæ°é¨å
# =========================
K = 97.5            # è¡æä»·
r = 0.043           # å©ç
T = 0.58            # å©ä½å¹´é
S_low, S_high = 70, 140  # æ çä»·èå´
S_target = 110      # éè¦æ¥ delta çç¹å®æ çä»·æ ¼
sigma_target = 0.276  # éè¦æ¥ delta çç¹å®æ³¢å¨ç

# æ³¢å¨çåè¡¨ ââ å¯å¨æ­¤å¤å¢åæä¿®æ¹æ°å¼
sigma_list = [0.15, 0.276, 0.40]

# =========================
# è®¡ç® deltaï¼æ¬§å¼çæ¶¨ææï¼
# =========================
def delta_call(S, K, r, T, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return norm.cdf(d1)

# çææ çä»·æ ¼ç½æ ¼
S_range = np.linspace(S_low, S_high, 200)

# ç»å¾
plt.figure(figsize=(10, 6))
for sigma in sigma_list:
    deltas = delta_call(S_range, K, r, T, sigma)
    plt.plot(S_range, deltas, linewidth=2, label=f'Ï = {sigma*100:.1f}%')

plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Delta vs Spot Price (Call Option)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ä¿å­å¾ç
figure_path = 'delta_vs_spot.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# è®¡ç®ç¹å®ç¹ç delta
delta_at_s110 = delta_call(S_target, K, r, T, sigma_target)

# =========================
# æè¦æ±æå»ºè¾åºå­å
# =========================
result = {
    'delta_at_s110': round(delta_at_s110, 6),   # ä¿ç6ä½å°æ°
    'figure_path': figure_path
}

# ä»ç¨äºæ¼ç¤ºï¼å¦æç´æ¥è¿è¡ï¼å¯æå° result
if __name__ == '__main__':
    print(result)

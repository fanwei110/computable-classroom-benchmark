import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ============================
# å¯è°åæ°åº
# ============================
# è¡æä»·
K = 97.5
# æ é£é©å©ç (å¹´å)
r = 0.043
# å©ä½å°ææ¶é´ (å¹´)
T = 0.58
# æ³¢å¨çåè¡¨ (å¯èªè¡å¢åãä¿®æ¹)
VOLATILITIES = [0.15, 0.276, 0.40]
# æ çèµäº§ä»·æ ¼åºé´
S_MIN, S_MAX = 70, 140
# éè¦åç¬æ¥å delta çæ çä»·æ ¼åæ³¢å¨ç
S_REPORT = 110
SIGMA_REPORT = 0.276
# å¾çä¿å­è·¯å¾
FIG_PATH = "delta_plot.png"

# ============================
# Black-Scholes çæ¶¨ææ Delta
# ============================
def bs_call_delta(S, K, T, r, sigma):
    """è®¡ç®æ¬§å¼çæ¶¨ææ delta (N(d1))ï¼S å¯ä¸ºæ éææ°ç»ã"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ============================
# è®¡ç®å¹¶ç»å¾
# ============================
S_grid = np.linspace(S_MIN, S_MAX, 300)

plt.figure(figsize=(10, 6))
for sigma in VOLATILITIES:
    delta = bs_call_delta(S_grid, K, T, r, sigma)
    plt.plot(S_grid, delta, label=f"Ï = {sigma*100:.1f}%")

# å¨ S=110, Ï=27.6% å¤æ è®°ä¸ç¹
delta_at_s110 = bs_call_delta(S_REPORT, K, T, r, SIGMA_REPORT)
plt.scatter(S_REPORT, delta_at_s110, color='red', zorder=5)
plt.annotate(f"({S_REPORT}, {delta_at_s110:.4f})",
             (S_REPORT, delta_at_s110),
             textcoords="offset points",
             xytext=(10, -10),
             fontsize=9,
             color='red')

plt.xlabel("æ çèµäº§ä»·æ ¼ S")
plt.ylabel("Delta")
plt.title("æ¬§å¼çæ¶¨ææ Delta æ²çº¿ (Black-Scholes)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(FIG_PATH, dpi=150)
plt.close()

# ============================
# è¾åºç»æå­å
# ============================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': FIG_PATH
}

# å¦æç´æ¥è¿è¡èæ¬ï¼å¯ä»¥æå°ç»æä»¥æ¹ä¾¿æ¥ç
if __name__ == "__main__":
    print(result)

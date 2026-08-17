import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ========== å¯è°åæ° ==========
K = 97.5            # è¡æä»·
r = 0.043           # æ é£é©å©çï¼è¿ç»­å¤å©ï¼å°æ°å½¢å¼ï¼
T = 0.58            # å©ä½å¹´é
sigma_list = [0.15, 0.276, 0.40]  # æ³¢å¨çåæ°ï¼å¯è°ï¼
S0 = 110.0          # è®¡ç® delta æ¶çæ çä»·æ ¼
sigma_target = 0.276 # è®¡ç® delta æ¶ä½¿ç¨çæ³¢å¨ç

# ====== è®¡ç® deltaï¼çæ¶¨ææï¼=======
def delta_call(S, K, r, sigma, T):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# æå®ç¹ç delta
delta_110 = delta_call(S0, K, r, sigma_target, T)

# ====== ç»å¾ ======
S = np.linspace(70, 140, 200)
plt.figure(figsize=(8, 5))
for sigma in sigma_list:
    plt.plot(S, delta_call(S, K, r, sigma, T), label=f'$\sigma$={sigma*100:.1f}%')
plt.xlabel('æ çä»·')
plt.ylabel('Delta')
plt.title('çæ¶¨ææ Delta éæ çä»·æ ¼åå')
plt.legend()
plt.grid(True)

# ä¿å­å¾ç
fig_path = 'delta_plot.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# ====== è¾åºç»æ ======
result = {
    'delta_at_s110': delta_110,
    'figure_path': fig_path
}

print(result)

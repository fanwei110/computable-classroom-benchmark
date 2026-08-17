import numpy as np
from scipy.stats import norm

# è¾ååæ°
S = 103.7      # æ çç°ä»·
K = 97.5       # è¡æä»·
sigma = 0.276  # å¹´åæ³¢å¨ç
r = 0.043      # æ é£é©å©ç
T = 0.58       # å©ä½æéï¼å¹´ï¼

# è®¡ç® d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

# è®¡ç® vegaï¼æ³¢å¨çåå1åä½çä»·æ ¼ååï¼
vega = S * np.sqrt(T) * norm.pdf(d1)

# éå«æ³¢å¨çä¸åä¸ä¸ªç¾åç¹ï¼å³ +0.01ï¼æ¶ï¼ææä»·æ ¼çåå
delta_sigma = 0.01
price_change = vega * delta_sigma

# ç»æå­åå­å
result = {'price_change': price_change}

# è¾åºï¼æ¹ä¾¿è¯¾å æ¥ç
print(f"Vega: {vega:.6f}")
print(f"æ³¢å¨çä¸å1ä¸ªç¾åç¹çä»·æ ¼åå: {price_change:.6f}")
print(f"ç»æå­å: {result}")

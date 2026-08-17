import numpy as np
from scipy.stats import norm

# å·²ç¥åæ°
S = 103.7          # æ çä»·æ ¼
K = 97.5           # è¡æä»·
sigma = 0.276      # éå«æ³¢å¨çï¼å°æ°ï¼
r = 0.043          # è¿ç»­å¤å©æ é£é©å©ç
T = 0.58           # å°ææ¶é´ï¼å¹´ï¼
delta_sigma = 0.01 # IVæ¶¨1ä¸ªç¹ï¼å³0.01

# è®¡ç® d1
d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
# è®¡ç® Vegaï¼å¯¹ sigma çåå¯¼æ°ï¼
vega = S * norm.pdf(d1) * np.sqrt(T)
# ä»·æ ¼åå = Vega * ÎÏ
price_change = vega * delta_sigma

result = {'price_change': price_change}
result

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. è¯»åçå®æ°æ®ï¼æ­¤å¤ç¨æ¨¡ææ°æ®ç¤ºæï¼
# df = pd.read_csv('data/market_snapshot_v1.csv')
# åè®¾ fund åæ¯æ¥æ¶ççï¼å°æ°ï¼
# returns = df['fund']

# ---- æ¨¡ææ°æ®ï¼æ¨æ¿æ¢ä¸ºçå®æ°æ®å³å¯ï¼----
np.random.seed(42)
returns = pd.Series(np.random.normal(0.0005, 0.02, 1000))  # æ¨¡æ1000å¤©æ¥æ¶ç

# 2. åæ°è®¾ç½®
confidence = 0.95          # å¯è°ç½®ä¿¡æ°´å¹³
position = 1_000_000       # å¤´å¯¸100ä¸
ddof = 1                   # æ ·æ¬æ åå·®

# 3. è®¡ç®æ¥æç
pnl = position * returns

# 4. åå²æ³ VaRï¼åä½æ°æ³ï¼æå¤±ä¸ºæ­£ï¼
var_loss = -np.quantile(pnl, 1 - confidence)
print(f"åå²æ³ 95% 1æ¥ VaRï¼{var_loss:,.2f} å")

# 5. ç»ç´æ¹å¾å¹¶æ åº VaR çº¿
plt.figure(figsize=(8,5))
plt.hist(pnl, bins=50, alpha=0.7, color='steelblue', edgecolor='white')
plt.axvline(-var_loss, color='red', linestyle='dashed', linewidth=2, 
            label=f'VaR 95% = {var_loss:,.0f} å')
plt.xlabel('æ¥æçï¼åï¼')
plt.ylabel('é¢æ°')
plt.title('åå²æ³æ¥æçåå¸')
plt.legend()
plt.tight_layout()

# ä¿å­å¾ç
fig_path = 'hist_var_95_1d.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# 6. æè¦æ±æé ç»æå­å
result = {
    'hist_var_95_1d': var_loss,
    'figure_path': fig_path
}
print(result)

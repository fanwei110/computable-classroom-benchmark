import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== åæ°ä¸çº¦å® ==========
POSITION = 1_000_000          # å¤´å¯¸ 100 ä¸
CONFIDENCE = 0.95             # ç½®ä¿¡åº¦ï¼å¯è°ï¼
VAR_PERCENTILE = 100 * (1 - CONFIDENCE)  # 5%

# ========== è¯»åæ°æ® ==========
df = pd.read_csv('data/market_snapshot_v1.csv')
returns = df['fund']          # æ¥æ¶ççï¼å°æ°å½¢å¼ï¼

# ========== è®¡ç®æç ==========
pnl = POSITION * returns      # æçåºå

# ========== åå²æ³ VaR ==========
var_cutoff = np.percentile(pnl, VAR_PERCENTILE)   # 5% åä½æ°ï¼éå¸¸ä¸ºè´å¼ï¼
hist_var_95_1d = -var_cutoff                      # VaR æ¥åä¸ºæ­£çæå¤±éé¢

# ========== ç»å¾ ==========
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.7)
plt.axvline(var_cutoff, color='red', linestyle='dashed', linewidth=2,
            label=f'95% 1-Day VaR: ${hist_var_95_1d:,.2f}')
plt.xlabel('Profit & Loss ($)')
plt.ylabel('Frequency')
plt.title('Historical P&L Distribution with 95% VaR')
plt.legend()

# ä¿å­å¾ç
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ========== è¾åºå­å ==========
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

print(result)

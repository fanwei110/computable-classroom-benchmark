import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- åæ° ----------
confidence = 0.95          # ç½®ä¿¡åº¦ï¼å¯è°ï¼
alpha = 1 - confidence     # æ¾èæ§æ°´å¹³
position = 1_000_000       # å¤´å¯¸ï¼åï¼
data_path = "data/market_snapshot_v1.csv"
figure_save_path = "var_histogram.png"

# ---------- è¯»åæ°æ® ----------
df = pd.read_csv(data_path)
# åè®¾æ¶ççå¨ 'fund' åï¼å½¢å¼ä¸ºå°æ°ï¼å¦0.01è¡¨ç¤º1%ï¼
returns = df['fund'].dropna()

# ---------- è®¡ç®æç ----------
pnl = position * returns   # æ¯æ¥æçï¼åï¼

# ---------- åå² VaR ----------
# å¨æ¾èæ§æ°´å¹³ alpha ä¸çåä½æ°ï¼æå¤±ä¸ºè´å¼ï¼VaRååç»å¯¹å¼ï¼
var_loss = -np.quantile(pnl, alpha)
print(f"åå²æ³ {confidence*100:.0f}% ä¸æ¥ VaR: {var_loss:,.2f} å")

# ---------- ç´æ¹å¾ ----------
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='steelblue', edgecolor='white', alpha=0.8, label='Daily P&L')
plt.axvline(x=-var_loss, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence*100:.0f}% 1-Day VaR: {var_loss:,.2f}')
plt.title('Historical VaR - Profit/Loss Distribution', fontsize=14)
plt.xlabel('Profit / Loss (CNY)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend()
plt.tight_layout()
plt.savefig(figure_save_path, dpi=150)
plt.close()

# ---------- è¾åºå­å ----------
result = {
    'hist_var_95_1d': var_loss,
    'figure_path': figure_save_path
}

# æå°ç»æï¼è¥å¨èæ¬ä¸­è¿è¡ï¼ä¼èªå¨æ¾ç¤ºï¼
print("\nResult Dictionary:")
print(result)

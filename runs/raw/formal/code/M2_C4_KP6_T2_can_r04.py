import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- å¯è°åæ° ----------
WINDOW = 60                 # æ»å¨çªå£é¿åº¦ï¼äº¤ææ¥ï¼
ANNUAL_RISK_FREE = 0.021    # å¹´åæ é£é©å©çï¼å°æ°ï¼
TRADING_DAYS = 252          # å¹´äº¤ææ¥å¤©æ°
# ----------------------------

# 1. è¯»åæ°æ®
df = pd.read_csv('data/market_snapshot_v1.csv')

# å°è¯èªå¨è¯å«æ¥æå
date_cols = ['date', 'Date', 'time', 'timestamp']
date_col = None
for col in date_cols:
    if col in df.columns:
        date_col = col
        break

if date_col is not None:
    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)
else:
    # è¥æ æ¥æåï¼ä¿çé»è®¤æ´æ°ç´¢å¼
    pass

# ç¡®ä¿ fund åä¸ºæ°å¼
df['fund'] = pd.to_numeric(df['fund'], errors='coerce')

# 2. è®¡ç®æ¥åº¦æ é£é©å©çåè¶æ¶ç
rf_daily = ANNUAL_RISK_FREE / TRADING_DAYS
excess_return = df['fund'] - rf_daily

# 3. æ»å¨è®¡ç®ï¼åå¼ä¸æ åå·®ï¼æ ·æ¬ï¼ddof=1ï¼
roll_mean = excess_return.rolling(window=WINDOW).mean()
roll_std  = excess_return.rolling(window=WINDOW).std(ddof=1)

# 4. å¹´åå¤æ®æ¯ç = sqrt(252) * (æ¥åè¶ / æ¥æ åå·®)
annual_sharpe = np.sqrt(TRADING_DAYS) * (roll_mean / roll_std)

# 5. æåæåä¸ä¸ªçªå£çå¤æ®å¼
valid_sharpe = annual_sharpe.dropna()
if len(valid_sharpe) == 0:
    raise ValueError("æ°æ®ä¸è¶³ä»¥è®¡ç®è³å°ä¸ä¸ªçªå£çå¤æ®æ¯çã")
rolling_sharpe_last = float(valid_sharpe.iloc[-1])

# 6. ç»å¶æ¶é´åºåå¾
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(annual_sharpe.index, annual_sharpe.values, color='steelblue', linewidth=1.0)
ax.set_title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio')
ax.set_xlabel('Date' if date_col else 'Index')
ax.set_ylabel('Sharpe Ratio')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.grid(True, alpha=0.3)
fig.tight_layout()

# ä¿å­å¾ç
figure_path = f'rolling_sharpe_{WINDOW}d.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# 7. å¡«åç»æå­å
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# å±ç¤ºç»æï¼æå¸è¯¾ä¸å¯è§ï¼
print(result)

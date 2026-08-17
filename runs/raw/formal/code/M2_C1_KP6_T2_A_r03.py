import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- åæ° ----------
window = 60          # æ»å¨çªå£ï¼äº¤ææ¥ï¼
rf_annual = 0.021    # å¹´åæ é£é©å©ç
# ------------------------

# æ¨¡æ fund åå¼æ°æ®ï¼æ¿æ¢ä¸ºçå®æ°æ®ï¼
np.random.seed(42)
dates = pd.date_range('2022-01-01', periods=252, freq='B')
nav = 100 * (1 + np.random.normal(0.0005, 0.01, 252).cumprod())  # éæºåå¼
fund_series = pd.Series(nav, index=dates)

# è®¡ç®æ¥æ¶çç
daily_return = fund_series.pct_change().dropna()

# å¹´åæ é£é©å©çè½¬ä¸ºæ¥åº¦
rf_daily = rf_annual / 252

# è¶æ¶ç
excess_return = daily_return - rf_daily

# 60æ¥æ»å¨å¹´åå¤æ®æ¯ç
rolling_mean = excess_return.rolling(window).mean() * 252
rolling_std = excess_return.rolling(window).std() * np.sqrt(252)
rolling_sharpe = rolling_mean / rolling_std

# æåä¸ä¸ªçªå£æ°å¼
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ç»å¾
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe, label=f'{window}-Day Rolling Annualized Sharpe')
plt.axhline(0, color='gray', linestyle='--')
plt.title('Rolling Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()

fig_path = './rolling_sharpe_ratio.png'
plt.savefig(fig_path)
plt.close()

# ç»æå­å
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 4),
    'figure_path': fig_path
}

print(result)

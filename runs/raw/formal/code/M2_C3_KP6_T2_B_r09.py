import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# åæ°è®¾ç½®ï¼çªå£å¯è°ï¼
# =========================
window = 60                # æ»å¨çªå£ï¼å¯æ¹ä¸ºä»»ææ´æ°ï¼
rf_annual = 0.021          # å¹´åæ é£é©å©ç 2.1%
trading_days = 252         # æ¯å¹´äº¤ææ¥

# =========================
# ç¤ºä¾æ°æ®ï¼è¯·æ¿æ¢ä¸ºçå®æ°æ®ï¼
# =========================
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=500, freq='B')
returns = np.random.normal(0.0005, 0.01, len(dates))
fund_prices = 100 * np.exp(np.cumsum(returns))
df = pd.DataFrame({'fund': fund_prices}, index=dates)

# =========================
# è®¡ç®æ¥æ¶çç
# =========================
df['daily_return'] = df['fund'].pct_change()
rf_daily = rf_annual / trading_days   # æ¥åæ é£é©å©ç

# =========================
# æ»å¨å¤æ®æ¯çå½æ°
# =========================
def rolling_sharpe(return_series, window, rf_daily):
    roll_mean = return_series.rolling(window).mean()
    roll_std  = return_series.rolling(window).std(ddof=1)  # æ ·æ¬æ åå·®
    sharpe_annualized = (roll_mean - rf_daily) / roll_std * np.sqrt(trading_days)
    return sharpe_annualized

sharpe_series = rolling_sharpe(df['daily_return'], window, rf_daily)

# æåä¸ä¸ªçªå£çå¤æ®å¼ï¼å»é¤ NaNï¼
rolling_sharpe_last = sharpe_series.dropna().iloc[-1]

# =========================
# ç»å¾å¹¶ä¿å­
# =========================
fig_path = 'rolling_sharpe.png'
plt.figure(figsize=(10, 5))
plt.plot(sharpe_series.index, sharpe_series.values, label=f'{window}-Day Rolling Sharpe')
plt.axhline(y=0, color='gray', linestyle='--')
plt.title(f'{window}-Day Rolling Sharpe Ratio (Annualized)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()
plt.savefig(fig_path)
plt.show()

# =========================
# è¾åºç»æå­åå­å
# =========================
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 6),
    'figure_path': fig_path
}

print(result)

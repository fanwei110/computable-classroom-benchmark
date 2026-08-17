import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------- 参数 -------------
window = 60                # 滚动窗口（可调）
rf_annual = 0.021          # 年化无风险利率
trading_days = 252         # 年交易日
rf_daily = rf_annual / trading_days

# ------------- 模拟数据（请替换为你的真实 df）-------------
np.random.seed(42)
dates = pd.date_range('2022-01-01', '2024-12-31', freq='B')
prices = 100 * (1 + np.random.randn(len(dates)) * 0.01).cumprod()
df = pd.DataFrame({'fund': prices}, index=dates)

# ------------- 日收益率 -------------
df['return'] = df['fund'].pct_change()

# ------------- 滚动年化夏普 -------------
rolling_mean = df['return'].rolling(window).mean() * trading_days
rolling_std  = df['return'].rolling(window).std() * np.sqrt(trading_days)
df['rolling_sharpe'] = (rolling_mean - rf_annual) / rolling_std

# ------------- 最后一个窗口的夏普值 -------------
rolling_sharpe_last = round(df['rolling_sharpe'].iloc[-1], 6)

# ------------- 绘图并保存 -------------
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df.index, df['rolling_sharpe'], label=f'{window}-Day Rolling Sharpe', color='navy')
ax.axhline(0, color='gray', linestyle='--')
ax.set_title('60-Day Rolling Sharpe Ratio (Annualized)')
ax.set_ylabel('Sharpe Ratio')
ax.legend()
fig.tight_layout()
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ------------- 输出字典 -------------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

print(result)

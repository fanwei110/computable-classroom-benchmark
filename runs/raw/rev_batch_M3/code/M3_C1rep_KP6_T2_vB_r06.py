import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ── 生成示例数据（如有实际数据，替换此处即可）──────────────────────
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='B')
daily_ret = np.random.normal(0.0006, 0.014, len(dates))   # 日收益率
df = pd.DataFrame({'fund': daily_ret}, index=dates)

# ── 参数 ────────────────────────────────────────────────────────
window   = 60            # 可调窗口
rf_annual = 0.021        # 年化无风险利率 2.1%
rf_daily  = rf_annual / 252

# ── 计算滚动夏普（年化）────────────────────────────────────────
rolling_mean = df['fund'].rolling(window=window).mean()
rolling_std  = df['fund'].rolling(window=window).std()
rolling_sharpe = (rolling_mean - rf_daily) / rolling_std * np.sqrt(252)

# ── 最后一个窗口值 ─────────────────────────────────────────────
rolling_sharpe_last = float(rolling_sharpe.iloc[-1])

# ── 画图 ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(rolling_sharpe.index, rolling_sharpe.values,
        color='#1f77b4', linewidth=1.2,
        label=f'{window}-Day Rolling Sharpe (rf={rf_annual*100:.1f}%)')
ax.axhline(y=0, color='grey', linestyle='--', linewidth=0.8)

# 标注最后一个值
ax.scatter(rolling_sharpe.index[-1], rolling_sharpe_last,
           color='red', zorder=5, s=60)
ax.annotate(f'{rolling_sharpe_last:.4f}',
            xy=(rolling_sharpe.index[-1], rolling_sharpe_last),
            xytext=(-60, 20), textcoords='offset points',
            fontsize=11, color='red', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='red'))

ax.set_title(f'{window}-Day Rolling Sharpe Ratio  (rf = {rf_annual*100:.1f}%)',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.legend(fontsize=11, loc='upper left')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45)
plt.tight_layout()

fig_path = 'rolling_sharpe.png'
fig.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# ── 输出契约 ───────────────────────────────────────────────────
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': fig_path
}

print(result)

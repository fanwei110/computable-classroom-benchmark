import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ============================================================
# 数据准备（若无本地文件，则生成示例数据）
# ============================================================
np.random.seed(42)
dates = pd.date_range(start='2022-01-04', end='2024-12-31', freq='B')
fund_returns = np.random.normal(loc=0.0004, scale=0.014, size=len(dates))
df = pd.DataFrame({'fund': fund_returns}, index=dates)

# ============================================================
# 参数设置
# ============================================================
rf_annual = 0.021          # 年化无风险利率 2.1%
window    = 60             # 滚动窗口（可调）
rf_daily  = rf_annual / 252

# ============================================================
# 计算 60 天滚动夏普比率
# ============================================================
rolling_mean = df['fund'].rolling(window=window).mean()
rolling_std  = df['fund'].rolling(window=window).std()

# 年化滚动夏普 = (日均收益 - 日无风险) / 日标准差 × sqrt(252)
rolling_sharpe = ((rolling_mean - rf_daily) / rolling_std) * np.sqrt(252)

# ============================================================
# 最后一个窗口的值
# ============================================================
rolling_sharpe_last = float(rolling_sharpe.iloc[-1])

# ============================================================
# 绘图
# ============================================================
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(rolling_sharpe.index, rolling_sharpe.values,
        color='#2C73D2', linewidth=1.0, label=f'{window}-Day Rolling Sharpe')
ax.axhline(y=0, color='#E74C3C', linestyle='--', linewidth=0.8, alpha=0.7, label='Sharpe = 0')

# 标注最后一个值
last_date = rolling_sharpe.index[-1]
last_val  = rolling_sharpe.iloc[-1]
ax.scatter([last_date], [last_val], color='#E74C3C', s=60, zorder=5)
ax.annotate(f'{last_val:.4f}',
            xy=(last_date, last_val),
            xytext=(-60, 20), textcoords='offset points',
            fontsize=10, fontweight='bold', color='#E74C3C',
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.2))

# 填充正负区域
ax.fill_between(rolling_sharpe.index, rolling_sharpe.values, 0,
                where=(rolling_sharpe.values >= 0),
                interpolate=True, alpha=0.15, color='#27AE60')
ax.fill_between(rolling_sharpe.index, rolling_sharpe.values, 0,
                where=(rolling_sharpe.values < 0),
                interpolate=True, alpha=0.15, color='#E74C3C')

ax.set_title(f'{window}-Day Rolling Sharpe Ratio  (rf = {rf_annual*100:.1f}%)',
             fontsize=15, fontweight='bold', pad=12)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45)
plt.tight_layout()

figure_path = 'rolling_sharpe_60d.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ============================================================
# 输出契约
# ============================================================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

print(f"最后一个窗口日期: {last_date.strftime('%Y-%m-%d')}")
print(f"滚动夏普比率终值: {rolling_sharpe_last:.6f}")
print(f"图表已保存至: {figure_path}")
print(f"\nresult = {result}")

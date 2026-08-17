import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============ 参数设置 ============
rf_annual = 0.021          # 无风险利率 2.1%（小数表示）
window = 60                 # 滚动窗口（可调）
trading_days = 252          # 年交易日数

# ============ 日度无风险利率（年复利 → 日复利）============
daily_rf = (1 + rf_annual) ** (1 / trading_days) - 1

# ============ 计算日收益率 ============
returns = df['fund'].pct_change().dropna()

# ============ 滚动 Sharpe ============
rolling_mean = returns.rolling(window=window).mean()
rolling_std  = returns.rolling(window=window).std(ddof=1)   # 样本标准量

# 年化滚动 Sharpe = (日均收益 - 日无风险) / 日标准差 × √252
rolling_sharpe = (rolling_mean - daily_rf) / rolling_std * np.sqrt(trading_days)

# ============ 最后一个窗口值 ============
last_value = rolling_sharpe.dropna().iloc[-1]

# ============ 画图 ============
fig, ax = plt.subplots(figsize=(12, 5))
rolling_sharpe.plot(ax=ax, color='steelblue', linewidth=1.2)
ax.axhline(y=0, color='red', linestyle='--', linewidth=0.8, alpha=0.6)
ax.set_title(f'{window}-Day Rolling Sharpe Ratio  (rf={rf_annual*100:.1f}%)', fontsize=13)
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.grid(True, alpha=0.3)
plt.tight_layout()

figure_path = 'rolling_sharpe.png'
fig.savefig(figure_path, dpi=150)
plt.close()

# ============ 输出 ============
result = {
    'rolling_sharpe_last': last_value,
    'figure_path': figure_path
}

print(f"最后一个窗口的滚动夏普值: {last_value:.6f}")
print(f"图片已保存至: {figure_path}")

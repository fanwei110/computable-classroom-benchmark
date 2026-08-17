import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------- 模拟数据（请替换为您的真实数据） ----------
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='B')
# 假设 fund 为日收益率（若不是收益率，请先用 pct_change() 转换）
fund_returns = pd.Series(np.random.normal(0.0005, 0.01, len(dates)), index=dates)

# ---------- 参数 ----------
window = 60          # 滚动窗口（可调）
rf_annual = 0.021    # 年化无风险利率
trading_days = 252   # 年交易日

rf_daily = rf_annual / trading_days   # 无风险日利率

# ---------- 计算滚动年化夏普 ----------
excess_returns = fund_returns - rf_daily

rolling_mean = excess_returns.rolling(window).mean() * trading_days  # 年化超额收益
rolling_std  = excess_returns.rolling(window).std() * np.sqrt(trading_days)  # 年化波动

rolling_sharpe = rolling_mean / rolling_std

# 最后一个窗口的夏普值
last_sharpe = rolling_sharpe.dropna().iloc[-1]
print(f"最后一个窗口的滚动年化夏普值: {last_sharpe:.4f}")

# ---------- 绘图 ----------
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe.dropna(), color='steelblue', linewidth=1.0)
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf=2.1%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
fig_path = 'rolling_sharpe.png'
plt.savefig(fig_path, dpi=150)
plt.show()

# ---------- 输出契约 ----------
result = {
    'rolling_sharpe_last': round(last_sharpe, 4),
    'figure_path': fig_path
}
print("结果字典:", result)

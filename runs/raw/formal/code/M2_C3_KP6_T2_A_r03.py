import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------- 模拟数据（实际使用时请替换为你的 fund 列）--------
np.random.seed(42)
dates = pd.bdate_range(start='2018-01-01', end='2024-12-31', freq='C', weekmask='Mon Tue Wed Thu Fri')
n = len(dates)
# 生成日收益率：均值约 0.0004，波动约 0.01
fund_returns = pd.Series(np.random.normal(0.0004, 0.01, n), index=dates)

# -------- 参数设置 --------
rf = 0.021         # 无风险利率
window = 60        # 滚动窗口（可调整）
trading_days = 252

# -------- 计算滚动年化夏普 --------
rolling_mean = fund_returns.rolling(window=window).mean()
rolling_std = fund_returns.rolling(window=window).std(ddof=1)

annualized_return = rolling_mean * trading_days
annualized_vol = rolling_std * np.sqrt(trading_days)

rolling_sharpe = (annualized_return - rf) / annualized_vol

# -------- 最后窗口的数值 --------
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# -------- 画图并保存 --------
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe, label='60-Day Rolling Annualized Sharpe', color='navy')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title(f'Rolling Annualized Sharpe Ratio (Window={window} days)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()
fig_path = 'rolling_sharpe.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# -------- 输出契约 --------
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 6),
    'figure_path': fig_path
}
print(result)

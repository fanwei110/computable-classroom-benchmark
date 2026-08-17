import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 生成示例数据：100个交易日的基金日收益率
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', periods=100, freq='B')
fund_returns = pd.Series(np.random.normal(0.001, 0.02, len(dates)), index=dates, name='fund')

# 参数设置
rf_annual = 0.021
rf_daily = rf_annual / 252
window = 60

# 计算60天滚动年化夏普比率
rolling_mean = fund_returns.rolling(window=window).mean()
rolling_std = fund_returns.rolling(window=window).std()
rolling_sharpe = (rolling_mean - rf_daily) / rolling_std * np.sqrt(252)

# 最后一个窗口值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# 绘图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe, label=f'{window}-Day Rolling Sharpe Ratio', color='blue')
plt.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
plt.title(f'Rolling Sharpe Ratio (rf={rf_annual*100}% annual, window={window} days)')
plt.xlabel('Date')
plt.ylabel('Annualized Sharpe Ratio')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图表
fig_path = 'rolling_sharpe.png'
plt.savefig(fig_path)
plt.close()

# 结果字典
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 4),
    'figure_path': fig_path
}

print(result)

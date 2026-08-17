import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并计算日无风险利率
data_path = Path('data/market_snapshot_v1.csv')
df = pd.read_csv(data_path, parse_dates=['date'], index_col='date')
daily_returns = df['fund'].dropna()  # 读取fund列日收益率
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252  # 日无风险利率

# 2. 计算滚动夏普比率
window_size = 60  # 可调窗口长度
excess_returns = daily_returns - daily_rf_rate  # 超额收益
rolling_mean = excess_returns.rolling(window=window_size).mean()
rolling_std = excess_returns.rolling(window=window_size).std(ddof=1)
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)  # 年化夏普比率

# 3. 报告最后一个窗口的值并绘图
last_sharpe = rolling_sharpe.iloc[-1]
plt.figure(figsize=(10, 6))
rolling_sharpe.plot(title=f'{window_size}-Day Rolling Annualized Sharpe Ratio')
plt.ylabel('Sharpe Ratio')
plt.grid(True)

# 保存图形
figure_path = Path('rolling_sharpe_ratio.png')
plt.savefig(figure_path)
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': float(last_sharpe),
    'figure_path': str(figure_path)
}

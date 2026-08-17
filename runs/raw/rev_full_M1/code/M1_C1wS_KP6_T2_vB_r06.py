import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取快照CSV数据（模拟数据，实际应用中应替换为真实CSV读取）
# 假设CSV包含日期和基金净值列，列名为'date'和'fund'
# 这里创建模拟数据以确保脚本自包含
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
n_days = len(dates)
fund_values = 100 + np.cumsum(np.random.randn(n_days) * 0.5)
data = pd.DataFrame({'date': dates, 'fund': fund_values})
data.set_index('date', inplace=True)

# 无风险利率（年化2.1%，转换为日利率）
annual_rf = 0.021
daily_rf = (1 + annual_rf) ** (1/252) - 1

# 2. 计算60日滚动年化夏普比率
window_size = 60
rolling_returns = data['fund'].pct_change().dropna()
excess_returns = rolling_returns - daily_rf

# 计算滚动夏普比率
def calculate_rolling_sharpe(excess_returns, window_size):
    rolling_mean = excess_returns.rolling(window=window_size).mean()
    rolling_std = excess_returns.rolling(window=window_size).std()
    rolling_sharpe = rolling_mean / rolling_std * np.sqrt(252)  # 年化
    return rolling_sharpe

rolling_sharpe = calculate_rolling_sharpe(excess_returns, window_size)

# 3. 报告最后一个窗口的值并绘图
last_sharpe = rolling_sharpe.iloc[-1]

# 绘图
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window_size}-Day Rolling Annualized Sharpe Ratio (rf={annual_rf*100:.1f}%)')
plt.ylabel('Sharpe Ratio')
plt.grid(True)

# 保存图形
figure_path = Path('rolling_sharpe.png')
plt.savefig(figure_path)
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': str(figure_path.absolute())
}

# 输出结果以供验证
print(result)

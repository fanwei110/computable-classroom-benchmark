import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. 读取数据并计算日无风险利率
data_path = Path('data/market_snapshot_v1.csv')
df = pd.read_csv(data_path, parse_dates=['date'])
daily_rf_rate = 0.021 / 252  # 年利率2.1%转换为日利率

# 提取基金日收益率
fund_returns = df['fund'].dropna().values  # 确保无缺失值
dates = df['date'].dropna().values[-len(fund_returns):]  # 对齐日期

# 设置滚动窗口长度（可调）
window_length = 60

# 2. 计算滚动夏普比率
def calculate_rolling_sharpe(returns, window, daily_rf):
    n = len(returns)
    rolling_sharpe = np.full(n, np.nan)

    for i in range(window - 1, n):
        window_returns = returns[i - window + 1 : i + 1]
        excess_returns = window_returns - daily_rf
        mean_excess = np.mean(excess_returns)
        std_excess = np.std(excess_returns, ddof=1)
        if std_excess != 0:
            rolling_sharpe[i] = mean_excess / std_excess * np.sqrt(252)
    return rolling_sharpe

rolling_sharpe = calculate_rolling_sharpe(fund_returns, window_length, daily_rf_rate)

# 3. 报告最后一个窗口的夏普值
last_sharpe = rolling_sharpe[-1]

# 绘制时间序列图
plt.figure(figsize=(10, 6))
plt.plot(dates[-len(rolling_sharpe):], rolling_sharpe, label=f'{window_length}-day Rolling Sharpe Ratio')
plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
plt.title(f'{window_length}-Day Rolling Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = Path('rolling_sharpe_ratio.png')
plt.savefig(figure_path)
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': float(last_sharpe),
    'figure_path': str(figure_path)
}

# 输出result以便课堂使用
print(result)

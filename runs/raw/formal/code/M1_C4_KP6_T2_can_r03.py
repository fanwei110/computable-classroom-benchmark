import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 读取数据并计算日无风险利率
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path, parse_dates=['date'])
daily_rf_rate = 0.021 / 252  # 年利率2.1%转换为日利率

# 提取基金日收益率
fund_returns = df['fund'].dropna().values
dates = df['date'].dropna().values[-len(fund_returns):]  # 对齐日期

# 2. 计算滚动夏普比率
window_size = 60  # 可调窗口长度
rolling_sharpe = []

for i in range(window_size, len(fund_returns)):
    window_returns = fund_returns[i-window_size:i]
    excess_returns = window_returns - daily_rf_rate
    mean_excess = np.mean(excess_returns)
    std_excess = np.std(excess_returns, ddof=1)
    annualized_sharpe = (mean_excess / std_excess) * np.sqrt(252)
    rolling_sharpe.append(annualized_sharpe)

# 3. 报告最后一个窗口的夏普值
last_sharpe = rolling_sharpe[-1] if rolling_sharpe else np.nan

# 准备绘图数据
plot_dates = dates[window_size:]
plot_sharpe = rolling_sharpe

# 绘制时间序列图
plt.figure(figsize=(10, 6))
plt.plot(plot_dates, plot_sharpe, label='60-Day Rolling Sharpe Ratio')
plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)
plt.title('60-Day Rolling Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图形
figure_dir = 'figures'
os.makedirs(figure_dir, exist_ok=True)
figure_path = os.path.join(figure_dir, 'rolling_sharpe_ratio.png')
plt.savefig(figure_path)
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': figure_path
}

# 输出result以便课堂展示
print(result)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 1. 读取快照CSV数据（模拟数据，实际使用时应替换为真实CSV读取）
# 假设CSV包含日期和基金净值列，列名为'date'和'fund'
# 这里创建模拟数据以确保脚本自包含
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
n = len(dates)
fund_values = 100 + np.cumsum(np.random.randn(n) * 0.5)
data = pd.DataFrame({'date': dates, 'fund': fund_values})
data.set_index('date', inplace=True)

# 无风险利率（年化2.1%）
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252  # 假设252交易日/年

# 2. 计算60日滚动年化夏普比率
window_size = 60
returns = data['fund'].pct_change().dropna()
excess_returns = returns - daily_rf_rate

# 计算滚动夏普比率
rolling_sharpe = (
    excess_returns.rolling(window=window_size)
    .mean() / excess_returns.rolling(window=window_size).std()
    * np.sqrt(252)  # 年化
)

# 3. 报告最后一个窗口的值
last_sharpe = rolling_sharpe.iloc[-1]
print(f"最后一个窗口的夏普比率: {last_sharpe:.4f}")

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe, label='60-Day Rolling Sharpe Ratio', color='royalblue')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title('60-Day Rolling Annualized Sharpe Ratio', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# 格式化y轴显示
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}'))

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': figure_path
}

# 输出结果以供验证
print(result)

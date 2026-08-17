import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 模拟数据生成（假设fund列为基金的日收益率）
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=len(dates))  # 日收益率
rf = 0.021  # 年化无风险收益率

# 计算60天滚动夏普比率
window = 60
rolling_returns = pd.Series(fund_returns, index=dates)
rolling_mean = rolling_returns.rolling(window=window).mean() * 252  # 年化收益
rolling_std = rolling_returns.rolling(window=window).std() * np.sqrt(252)  # 年化波动率
rolling_sharpe = (rolling_mean - rf) / rolling_std

# 获取最后一个窗口的夏普比率值
last_sharpe = rolling_sharpe.iloc[-1]

# 绘制图表
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window}天滚动夏普比率 (rf={rf*100:.1f}%)', label='滚动夏普比率')
plt.axhline(y=0, color='r', linestyle='--', label='零线')
plt.ylabel('夏普比率')
plt.legend()
plt.grid(True)

# 保存图表
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

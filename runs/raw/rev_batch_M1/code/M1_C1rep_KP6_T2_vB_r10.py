import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 模拟数据生成（假设fund列为基金的日收益率）
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2023-12-31')
fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=len(dates))  # 日收益率
rf = 0.021  # 年化无风险收益率

# 创建DataFrame
df = pd.DataFrame({'fund': fund_returns}, index=dates)

# 计算60天滚动夏普比率
window = 60  # 滚动窗口天数
daily_rf = (1 + rf) ** (1/252) - 1  # 日化无风险收益率

# 计算滚动夏普比率
rolling_sharpe = (df['fund'].rolling(window=window).mean() - daily_rf) / df['fund'].rolling(window=window).std() * np.sqrt(252)

# 获取最后一个窗口的夏普比率值
last_sharpe = rolling_sharpe.iloc[-1]

# 绘制图表
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window}天滚动夏普比率 (rf={rf*100}%)')
plt.ylabel('夏普比率')
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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 模拟数据生成（实际应用中请替换为真实数据）
np.random.seed(42)
dates = pd.date_range(end=pd.Timestamp.today(), periods=200, freq='D')
fund_returns = pd.Series(np.random.normal(0.0005, 0.01, len(dates)), index=dates)
rf = 0.021  # 无风险收益率2.1%

# 计算滚动夏普比率
window = 60  # 滚动窗口天数
rolling_returns = fund_returns.rolling(window=window)
rolling_mean = rolling_returns.mean()
rolling_std = rolling_returns.std()
rolling_sharpe = (rolling_mean - rf/252) / rolling_std * np.sqrt(252)  # 年化夏普比率

# 获取最后一个窗口的夏普比率值
last_sharpe = rolling_sharpe.iloc[-1]

# 绘制图表
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window}天滚动夏普比率 (rf={rf*100:.1f}%)', label='滚动夏普比率')
plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
plt.ylabel('夏普比率')
plt.grid(True, alpha=0.3)
plt.legend()

# 保存图表
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

# 创建结果字典
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

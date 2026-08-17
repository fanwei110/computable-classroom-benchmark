import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 模拟数据生成（假设您有实际的fund收益率数据）
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=300, freq='D')
fund_returns = pd.Series(np.random.normal(0.0005, 0.01, size=300), index=dates)  # 日收益率
rf = 0.021  # 无风险收益率2.1%

# 计算滚动夏普比率
window = 60  # 滚动窗口天数
rolling_sharpe = (fund_returns.rolling(window).mean() - rf/252) / fund_returns.rolling(window).std() * np.sqrt(252)

# 获取最后一个窗口的夏普值
last_sharpe = rolling_sharpe.iloc[-1]

# 绘制图表
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window}天滚动夏普比率 (rf={rf*100:.1f}%)')
plt.ylabel('夏普比率')
plt.grid(True)

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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 模拟数据生成（假设您有实际的fund收益率数据）
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=500)
fund_returns = pd.Series(np.random.normal(0.0005, 0.01, size=500), index=dates)  # 日收益率
rf = 0.021  # 无风险利率2.1%

# 计算60天滚动夏普比率
window = 60
rolling_returns = fund_returns.rolling(window=window)
excess_returns = rolling_returns.mean() - rf/252  # 假设年化无风险利率转换为日利率
volatility = rolling_returns.std()
rolling_sharpe = excess_returns / volatility * np.sqrt(252)  # 年化夏普比率

# 获取最后一个窗口的夏普比率值
last_sharpe = rolling_sharpe.dropna().iloc[-1]

# 绘制图表
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window}天滚动夏普比率 (rf={rf*100}%)', label='滚动夏普比率')
plt.axhline(y=0, color='r', linestyle='--', alpha=0.5)
plt.ylabel('夏普比率')
plt.legend()
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

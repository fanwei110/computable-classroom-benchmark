import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 模拟 fund 列数据（假设这是日收益率数据）
np.random.seed(42)
n_days = 200  # 总天数
fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益率

# 参数
rf = 0.021  # 无风险利率 2.1%
window = 60  # 滚动窗口（可调）

# 计算滚动年化夏普比率
def calculate_rolling_sharpe(returns, window, rf):
    rolling_mean = returns.rolling(window=window).mean() * 252  # 年化均值
    rolling_std = returns.rolling(window=window).std() * np.sqrt(252)  # 年化标准差
    rolling_sharpe = (rolling_mean - rf) / rolling_std
    return rolling_sharpe

# 计算滚动夏普比率
rolling_sharpe = calculate_rolling_sharpe(pd.Series(fund_returns), window, rf)

# 最后一个窗口的夏普比率
last_sharpe = rolling_sharpe.dropna().iloc[-1]

# 绘制曲线
plt.figure(figsize=(10, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe, label=f'{window}-day Rolling Annualized Sharpe Ratio')
plt.axhline(y=0, color='r', linestyle='--', label='Zero Line')
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf*100}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'rolling_sharpe_plot.png'
plt.savefig(figure_path)
plt.close()

# 输出结果
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

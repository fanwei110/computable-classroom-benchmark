import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def calculate_rolling_sharpe(fund_returns, rf=0.021, window=60):
    """
    计算滚动夏普比率

    参数:
    fund_returns: 基金收益率序列 (Series或list)
    rf: 无风险收益率 (年化)
    window: 滚动窗口长度 (天数)

    返回:
    滚动夏普比率序列和最后一个窗口的夏普比率
    """
    # 转换为Series
    fund_returns = pd.Series(fund_returns)

    # 计算日度超额收益
    daily_rf = (1 + rf) ** (1/252) - 1
    excess_returns = fund_returns - daily_rf

    # 计算滚动夏普比率
    rolling_mean = excess_returns.rolling(window).mean()
    rolling_std = excess_returns.rolling(window).std(ddof=1)
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return rolling_sharpe, rolling_sharpe.iloc[-1]

# 生成示例数据（如果没有实际数据）
np.random.seed(42)
n_days = 252 * 2  # 2年的数据
fund_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)

# 计算滚动夏普比率
rolling_sharpe, last_sharpe = calculate_rolling_sharpe(fund_returns, rf=0.021, window=60)

# 绘制图表
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe.values, label='60-day Rolling Sharpe Ratio')
plt.axhline(y=0, color='r', linestyle='--')
plt.title('60-Day Rolling Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
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

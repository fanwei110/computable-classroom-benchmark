import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_rolling_sharpe(fund_data, rf=0.021, window=60):
    """
    计算滚动年化夏普比率

    参数:
    fund_data: Series, 基金的日收益率数据
    rf: float, 无风险收益率（年化）
    window: int, 滚动窗口天数

    返回:
    Series, 滚动夏普比率
    """
    # 计算日超额收益率
    excess_returns = fund_data - rf/252

    # 计算滚动年化夏普比率
    rolling_mean = excess_returns.rolling(window=window).mean()
    rolling_std = excess_returns.rolling(window=window).std()
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return rolling_sharpe

# 示例数据（假设您有实际的fund数据）
# 这里创建一个示例数据集，实际使用时请替换为您的数据
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2023-12-31')
fund_returns = pd.Series(np.random.normal(0.0005, 0.01, len(dates)), index=dates)

# 计算滚动夏普比率
window = 60  # 可调窗口大小
rolling_sharpe = calculate_rolling_sharpe(fund_returns, rf=0.021, window=window)

# 获取最后一个窗口的数值
last_sharpe_value = rolling_sharpe.dropna().iloc[-1]

# 绘制图形
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window}日滚动年化夏普比率 (rf={2.1}%)')
plt.ylabel('夏普比率')
plt.grid(True)

# 保存图形
figure_path = 'rolling_sharpe_plot.png'
plt.savefig(figure_path)
plt.close()

# 创建结果字典
result = {
    'rolling_sharpe_last': last_sharpe_value,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（在实际使用中可能不需要print）
print(result)

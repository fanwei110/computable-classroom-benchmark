import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 输入数据（示例数据，请替换为实际fund列数据）
# 假设fund列是日收益率数据
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=500)
fund_returns = pd.Series(np.random.normal(0.0005, 0.01, size=500), index=dates)

# 参数设置
rf = 0.021  # 无风险收益率2.1%
window = 60  # 滚动窗口（可调）

def calculate_rolling_sharpe(returns, window, rf):
    """
    计算滚动年化夏普比率
    returns: 日收益率序列
    window: 滚动窗口长度
    rf: 年化无风险收益率
    """
    # 日化无风险收益率
    daily_rf = (1 + rf) ** (1/252) - 1

    # 滚动计算均值和标准差
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()

    # 年化夏普比率
    rolling_sharpe = (rolling_mean - daily_rf) / rolling_std * np.sqrt(252)

    return rolling_sharpe

# 计算滚动夏普比率
rolling_sharpe = calculate_rolling_sharpe(fund_returns, window, rf)

# 获取最后一个窗口的夏普比率值
last_sharpe = rolling_sharpe.dropna().iloc[-1]

# 绘制曲线图
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{window}-day Rolling Annualized Sharpe Ratio (rf={rf*100}%)')
plt.ylabel('Sharpe Ratio')
plt.grid(True)

# 保存图片
figure_path = 'rolling_sharpe_plot.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

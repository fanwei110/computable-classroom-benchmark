import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 假设 fund 是一个 pandas Series，包含基金的日收益率
# 这里用随机数据模拟
np.random.seed(42)
fund = pd.Series(np.random.normal(0.0005, 0.01, 1000))  # 模拟1000个交易日的日收益率

# 参数
rf = 0.021  # 无风险利率 2.1%
window = 60  # 滚动窗口大小
trading_days = 252  # 每年交易日数

# 计算滚动年化夏普比率
def calculate_rolling_sharpe(fund_returns, window, rf, trading_days):
    # 滚动年化收益率
    rolling_mean = fund_returns.rolling(window=window).mean() * trading_days
    # 滚动年化波动率
    rolling_std = fund_returns.rolling(window=window).std(ddof=1) * np.sqrt(trading_days)
    # 滚动夏普比率
    rolling_sharpe = (rolling_mean - rf) / rolling_std
    return rolling_sharpe

rolling_sharpe = calculate_rolling_sharpe(fund, window, rf, trading_days)

# 最后一个窗口的夏普比率
last_sharpe = rolling_sharpe.dropna().iloc[-1]

# 绘图
plt.figure(figsize=(10, 6))
rolling_sharpe.plot(label=f'{window}-day Rolling Annualized Sharpe Ratio')
plt.title(f'{window}-day Rolling Annualized Sharpe Ratio (rf={rf*100}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid()

# 保存图片
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

# 输出结果
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 示例数据，假设fund是一个包含基金每日净值的Series
# 这里用随机数据模拟，实际应用中请替换为真实数据
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', periods=500)
fund = pd.Series(np.cumprod(1 + np.random.normal(0.0005, 0.01, size=500)), index=dates)

# 无风险利率
rf = 0.021

# 计算每日收益率
daily_returns = fund.pct_change().dropna()

# 计算滚动年化夏普比率
def rolling_sharpe(returns, window=60, rf=0.021):
    # 滚动年化收益率
    rolling_mean = returns.rolling(window=window).mean() * 252
    # 滚动年化波动率
    rolling_vol = returns.rolling(window=window).std(ddof=1) * np.sqrt(252)
    # 滚动夏普比率
    rolling_sharpe_ratio = (rolling_mean - rf) / rolling_vol
    return rolling_sharpe_ratio

# 计算60日滚动夏普比率
window = 60
sharpe_ratios = rolling_sharpe(daily_returns, window=window, rf=rf)

# 最后一个窗口的夏普比率
last_sharpe = sharpe_ratios.iloc[-1]

# 绘制曲线图
plt.figure(figsize=(10, 6))
sharpe_ratios.plot(title=f'{window}-day Rolling Annualized Sharpe Ratio')
plt.ylabel('Sharpe Ratio')
plt.xlabel('Date')

# 保存图片
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path)
plt.close()

# 输出结果
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

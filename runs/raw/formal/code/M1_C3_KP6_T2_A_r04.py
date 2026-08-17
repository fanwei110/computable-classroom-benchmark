import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# 示例数据（假设fund是日收益率，如果不是需要先转换）
# 这里假设fund是一个Series或DataFrame的一列
# 例如：fund = pd.Series(np.random.normal(0.001, 0.01, 1000))  # 模拟日收益率
# 实际使用时，请替换为真实数据
np.random.seed(42)
fund = pd.Series(np.random.normal(0.0005, 0.01, 1000))  # 模拟日收益率

# 参数
rf = 0.021  # 无风险利率
window = 60  # 滚动窗口
trading_days = 252  # 年化交易日

# 计算滚动年化夏普比率
def calculate_rolling_sharpe(fund_returns, window, rf, trading_days):
    rolling_mean = fund_returns.rolling(window=window).mean() * trading_days
    rolling_std = fund_returns.rolling(window=window).std(ddof=1) * np.sqrt(trading_days)
    rolling_sharpe = (rolling_mean - rf) / rolling_std
    return rolling_sharpe

rolling_sharpe = calculate_rolling_sharpe(fund, window, rf, trading_days)

# 最后一个窗口的夏普比率
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(rolling_sharpe, label=f'{window}-day Rolling Annualized Sharpe Ratio')
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
plt.title(f'{window}-day Rolling Annualized Sharpe Ratio (rf={rf*100}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path)
plt.close()

# 输出结果
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': os.path.abspath(figure_path)
}

print(result)

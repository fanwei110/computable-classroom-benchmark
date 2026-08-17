import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 设定参数
WINDOW_DAYS = 60  # 滚动窗口长度（可调）
ANNUAL_RISK_FREE_RATE = 0.021  # 年化无风险利率
DAILY_RISK_FREE_RATE = ANNUAL_RISK_FREE_RATE / 252  # 日化无风险利率（假设252交易日/年）

# 1. 读取数据
data_path = Path('data/market_snapshot_v1.csv')
df = pd.read_csv(data_path, parse_dates=['date'])
df.set_index('date', inplace=True)

# 提取基金日收益率（假设列名为'fund'）
fund_returns = df['fund'].dropna()

# 2. 计算滚动年化夏普比率
def calculate_rolling_sharpe(returns, window_days, daily_rf_rate):
    # 计算超额收益
    excess_returns = returns - daily_rf_rate

    # 滚动计算均值和标准差
    rolling_mean = excess_returns.rolling(window=window_days).mean()
    rolling_std = excess_returns.rolling(window=window_days).std()

    # 年化夏普比率
    annualized_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

    return annualized_sharpe

rolling_sharpe = calculate_rolling_sharpe(fund_returns, WINDOW_DAYS, DAILY_RISK_FREE_RATE)

# 3. 报告最后一个窗口的值
last_sharpe = rolling_sharpe.iloc[-1]

# 绘制时间序列图
plt.figure(figsize=(12, 6))
rolling_sharpe.plot(title=f'{WINDOW_DAYS}-Day Rolling Annualized Sharpe Ratio')
plt.ylabel('Sharpe Ratio')
plt.grid(True)

# 保存图形
figure_path = Path('rolling_sharpe_ratio.png')
plt.savefig(figure_path)
plt.close()

# 4. 填充result字典
result = {
    'rolling_sharpe_last': last_sharpe,
    'figure_path': str(figure_path)
}

# 输出结果（供教师查看）
print(result)

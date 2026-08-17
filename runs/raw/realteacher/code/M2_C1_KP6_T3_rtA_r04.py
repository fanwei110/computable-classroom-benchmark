import numpy as np

# 这里用 daily_returns 代表 fund 列的日收益率序列，您需要替换为实际数据
# daily_returns = df['fund'].values

# 假设您已经有 daily_returns 数据，例如：
# daily_returns = np.array([...])   # 请用实际数据替代

# 无风险年化利率
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 计算日超额收益
excess_returns = daily_returns - rf_daily

# 计算年化夏普
sharpe_annual = np.sqrt(trading_days) * (np.mean(excess_returns) / np.std(excess_returns, ddof=1))

result = {'sharpe_annual': sharpe_annual}

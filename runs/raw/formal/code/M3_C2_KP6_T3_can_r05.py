import pandas as pd
import numpy as np

# --- 假设说明 ---
# 1. 假设 CSV 中的 `fund` 列为基金净值（NAV）序列，据此计算日度简单收益率。
# 2. 假设数据频率为日频，一年按 252 个交易日进行年化处理（符合业界与教学常用标准）。
# 3. 无风险利率 2.1% 视为年化百分比利率，日度无风险利率 = 2.1% / 252。

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列并计算日度简单收益率
fund_nav = df['fund']
daily_returns = fund_nav.pct_change().dropna()

# 2. 计算全样本年化夏普比率
rf_annual = 0.021
trading_days_per_year = 252

# 计算日度平均收益率与标准差
mean_daily_return = daily_returns.mean()
std_daily_return = daily_returns.std()

# 年化处理
mean_annual_return = mean_daily_return * trading_days_per_year
std_annual_return = std_daily_return * np.sqrt(trading_days_per_year)

# 计算夏普比率：(年化超额收益) / (年化总风险)
# 年化超额收益 = 年化组合收益 - 年化无风险利率
sharpe_annual = (mean_annual_return - rf_annual) / std_annual_return

# 3. 把结果存入 result
result = {'sharpe_annual': sharpe_annual}

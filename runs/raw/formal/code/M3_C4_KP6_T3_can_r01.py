import pandas as pd
import numpy as np

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列并去除可能存在的缺失值
daily_returns = df['fund'].dropna().values

# 2. 计算日超额收益
rf_annual = 0.021  # 2.1% 的年无风险利率
rf_daily = rf_annual / 252  # 根据课程约定，日利率 = 年利率 / 252
excess_returns = daily_returns - rf_daily

# 3. 计算全样本夏普比率并年化
mean_excess = np.mean(excess_returns)
std_excess = np.std(excess_returns, ddof=1)  # 根据课程约定，使用样本标准差 (ddof=1)

sharpe_daily = mean_excess / std_excess
sharpe_annual = sharpe_daily * np.sqrt(252)  # 根据课程约定，按 sqrt(252) 年化

# 4. 把结果存入字典
result = {'sharpe_annual': sharpe_annual}

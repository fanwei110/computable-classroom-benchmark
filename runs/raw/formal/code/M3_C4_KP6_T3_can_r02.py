import pandas as pd
import numpy as np

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列的日收益率
daily_returns = df['fund']

# 给定年化无风险利率为 2.1%，按课程约定折算为日无风险利率
annual_rf = 0.021
daily_rf = annual_rf / 252

# 计算日超额收益
excess_returns = daily_returns - daily_rf

# 2. 计算全样本夏普比率
# 计算日超额收益的均值与样本标准差（ddof=1）
mean_excess = np.mean(excess_returns)
std_excess = np.std(excess_returns, ddof=1)

# 日夏普比率
daily_sharpe = mean_excess / std_excess

# 按课程约定进行年化（乘以 sqrt(252)）
sharpe_annual = daily_sharpe * np.sqrt(252)

# 3. 把结果存入字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)

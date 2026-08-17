import pandas as pd
import numpy as np

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 课程约定参数
rf_annual = 0.021       # 年化无风险利率 2.1%
trading_days = 252      # 每年交易日数

# 2. 计算日无风险利率（简单除法）
rf_daily = rf_annual / trading_days

# 3. 提取 fund 列的日收益，并减去日无风险利率得到日超额收益
daily_returns = df['fund']
daily_excess_returns = daily_returns - rf_daily

# 4. 计算日超额收益的均值与样本标准差（ddof=1）
mean_excess_daily = np.mean(daily_excess_returns)
std_excess_daily = np.std(daily_excess_returns, ddof=1)

# 5. 计算全样本夏普比率并年化（乘以 sqrt(252)）
sharpe_daily = mean_excess_daily / std_excess_daily
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 6. 将结果存入字典，键名严格为 'sharpe_annual'
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果以供课堂投屏展示
print(f"年化夏普比率: {result['sharpe_annual']:.4f}")
print(f"result = {result}")

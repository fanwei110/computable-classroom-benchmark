import pandas as pd
import numpy as np

# ==========================================
# 第一部分：计算年化夏普比率
# ==========================================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益
fund_daily_returns = df['fund']

# 无风险利率年化为 2.1%，折算到日（简单除法）
rf_annual = 0.021
rf_daily = rf_annual / 252

# 2. 计算日超额收益
excess_daily_returns = fund_daily_returns - rf_daily

# 计算日超额收益的样本均值和样本标准差 (ddof=1)
mean_excess_daily = np.mean(excess_daily_returns)
std_excess_daily = np.std(excess_daily_returns, ddof=1)

# 计算夏普比率并年化（乘以 sqrt(252)）
sharpe_daily = mean_excess_daily / std_excess_daily
sharpe_annual = sharpe_daily * np.sqrt(252)

# ==========================================
# 第二部分：Brinson-Hood-Beebower 业绩归因
# ==========================================

# 组合与基准的权重和收益
wp = np.array([0.45, 0.35, 0.20])
rp = np.array([0.083, 0.021, -0.014])

wb = np.array([0.40, 0.40, 0.20])
rb = np.array([0.067, 0.034, -0.009])

# 3. 按照约定公式计算三大效应
allocation_effect = np.sum((wp - wb) * rb)
selection_effect = np.sum(wb * (rp - rb))
interaction_effect = np.sum((wp - wb) * (rp - rb))

# ==========================================
# 第四部分：填充结果字典
# ==========================================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

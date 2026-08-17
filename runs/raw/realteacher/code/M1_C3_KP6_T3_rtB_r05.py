import numpy as np

# 假设 fund_returns 是基金的日收益率序列（小数形式）
# 示例：fund_returns = np.array([0.001, -0.002, 0.003, ...])

# 无风险利率（年化）
risk_free_rate_annual = 0.021

# 计算日无风险利率（按 252 个交易日复利）
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 计算日超额收益
excess_returns_daily = fund_returns - risk_free_rate_daily

# 计算日超额收益的均值和标准差（样本标准差，ddof=1）
mean_excess_daily = np.mean(excess_returns_daily)
std_excess_daily = np.std(excess_returns_daily, ddof=1)

# 年化处理
mean_excess_annual = mean_excess_daily * 252
std_excess_annual = std_excess_daily * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = mean_excess_annual / std_excess_annual

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

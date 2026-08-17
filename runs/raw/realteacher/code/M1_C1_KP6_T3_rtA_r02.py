import numpy as np

# 假设 daily_returns 是 fund 列的日收益数据（例如 pandas Series）
# 无风险利率（年化）为 2.1%
risk_free_rate_annual = 0.021

# 计算日化无风险利率
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 计算日超额收益
excess_returns_daily = daily_returns - risk_free_rate_daily

# 计算日超额收益的均值和标准差
mean_excess_return_daily = excess_returns_daily.mean()
std_excess_return_daily = excess_returns_daily.std()

# 年化夏普比率
sharpe_ratio_annual = (mean_excess_return_daily / std_excess_return_daily) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_ratio_annual
}

import numpy as np

# 无风险收益率（年化）
risk_free_rate_annual = 0.021
# 转换为日无风险收益率
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 计算日超额收益
excess_returns_daily = daily_returns - risk_free_rate_daily

# 计算日超额收益的均值和标准差
mean_excess_return_daily = excess_returns_daily.mean()
std_excess_return_daily = excess_returns_daily.std()

# 年化夏普比率
sharpe_annual = (mean_excess_return_daily / std_excess_return_daily) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

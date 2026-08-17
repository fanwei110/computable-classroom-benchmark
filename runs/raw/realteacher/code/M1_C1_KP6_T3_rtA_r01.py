import numpy as np

# 假设 daily_returns 是 fund 列的日收益数据（Series 或 list）
# 无风险利率（年化）为 2.1%
risk_free_rate_annual = 0.021

# 计算日化无风险利率
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 计算日超额收益
excess_returns = daily_returns - risk_free_rate_daily

# 计算年化夏普比率
sharpe_annual = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

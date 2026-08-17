import numpy as np

# 假设 daily_returns 是 fund 列的日收益率数据
mean_daily_return = daily_returns.mean()
std_daily_return = daily_returns.std(ddof=1)  # 样本标准差

annualized_return = mean_daily_return * 252
annualized_volatility = std_daily_return * np.sqrt(252)
excess_return = annualized_return - 0.021  # 无风险收益率 2.1%

sharpe_annual = excess_return / annualized_volatility

result = {
    'sharpe_annual': sharpe_annual
}

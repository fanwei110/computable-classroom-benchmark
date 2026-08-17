import numpy as np

# 第一问：年化夏普比率
# 假设 fund 列的日收益数据为 daily_returns（示例数据，实际应替换为真实数据）
daily_returns = np.array([0.001, -0.0005, 0.002, ...])  # 示例数据，需替换为实际数据
annual_risk_free_rate = 0.021
daily_risk_free_rate = annual_risk_free_rate / 252  # 假设一年252个交易日

# 计算超额收益
excess_returns = daily_returns - daily_risk_free_rate

# 年化收益和年化波动率
annualized_return = np.mean(daily_returns) * 252
annualized_volatility = np.std(daily_returns) * np.sqrt(252)

# 年化夏普比率
sharpe_annual = (annualized_return - annual_risk_free_rate) / annualized_volatility

# 第二问：业绩归因
# 组合和基准的权重和收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 总收益差异
total_effect = np.sum(portfolio_weights * portfolio_returns) - np.sum(benchmark_weights * benchmark_returns)

# 配置效应（Allocation Effect）
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * benchmark_returns)

# 选择效应（Selection Effect）
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 交互效应（Interaction Effect）
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

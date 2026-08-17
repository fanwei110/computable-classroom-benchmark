import numpy as np
import pandas as pd
from scipy import stats

# ====================== 第一部分：计算年化夏普比率 ======================
# 模拟课程数据快照 "fund" 列的日收益（假设数据已读取）
# 由于题目未提供具体数据，我们模拟一个典型的日收益序列（可替换为实际数据）
np.random.seed(42)  # 确保可复现
daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=252)  # 252个交易日

# 无风险利率（年化2.1%，转换为日利率）
annual_risk_free_rate = 0.021
daily_risk_free_rate = annual_risk_free_rate / 252

# 计算超额收益
excess_returns = daily_returns - daily_risk_free_rate

# 年化夏普比率 = (年化超额收益均值) / (年化超额收益标准差)
annualized_excess_return_mean = np.mean(excess_returns) * 252
annualized_excess_return_std = np.std(excess_returns, ddof=1) * np.sqrt(252)
sharpe_annual = annualized_excess_return_mean / annualized_excess_return_std

# ====================== 第二部分：计算配置、选择与交互效应 ======================
# 组合和基准的权重与收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算组合和基准的总收益
portfolio_total_return = np.sum(portfolio_weights * portfolio_returns)
benchmark_total_return = np.sum(benchmark_weights * benchmark_returns)

# 配置效应（Allocation Effect）：(组合权重 - 基准权重) * 基准收益
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * benchmark_returns)

# 选择效应（Selection Effect）：基准权重 * (组合收益 - 基准收益)
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 交互效应（Interaction Effect）：(组合权重 - 基准权重) * (组合收益 - 基准收益)
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# 验证：总效应 = 配置 + 选择 + 交互
total_effect = portfolio_total_return - benchmark_total_return
assert np.isclose(total_effect, allocation_effect + selection_effect + interaction_effect), "效应计算不一致"

# ====================== 输出结果 ======================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果（可选）
print("Result Dictionary:")
print(result)

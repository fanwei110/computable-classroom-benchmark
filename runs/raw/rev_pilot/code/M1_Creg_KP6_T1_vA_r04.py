import numpy as np
import pandas as pd
from scipy import stats

# ====================== 第一部分：计算年化夏普比率 ======================
# 模拟课程数据快照 "fund" 列的日收益（假设数据已加载）
# 由于题目未提供具体数据，我们模拟一个典型的日收益序列（可替换为实际数据）
np.random.seed(42)  # 确保可复现
n_days = 252  # 一年的交易日天数
daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 日收益均值0.05%，波动率1%

# 无风险利率（年化）
risk_free_rate_annual = 0.021
risk_free_rate_daily = risk_free_rate_annual / 252  # 日化无风险利率

# 计算年化夏普比率
excess_daily_returns = daily_returns - risk_free_rate_daily
sharpe_ratio_annual = np.sqrt(252) * np.mean(excess_daily_returns) / np.std(excess_daily_returns, ddof=1)

# ====================== 第二部分：计算配置、选择与交互效应 ======================
# 组合与基准的权重和收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算组合和基准的总收益
portfolio_total_return = np.sum(portfolio_weights * portfolio_returns)
benchmark_total_return = np.sum(benchmark_weights * benchmark_returns)

# 计算配置效应（Allocation Effect）
allocation_effect = np.sum(
    (portfolio_weights - benchmark_weights) * benchmark_returns
)

# 计算选择效应（Selection Effect）
selection_effect = np.sum(
    benchmark_weights * (portfolio_returns - benchmark_returns)
)

# 计算交互效应（Interaction Effect）
interaction_effect = np.sum(
    (portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns)
)

# 验证：总效应 = 配置 + 选择 + 交互
total_effect = portfolio_total_return - benchmark_total_return
assert np.isclose(total_effect, allocation_effect + selection_effect + interaction_effect), "效应分解不匹配"

# ====================== 输出结果 ======================
result = {
    'sharpe_annual': sharpe_ratio_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果（可选）
print("Result Dictionary:")
print(result)

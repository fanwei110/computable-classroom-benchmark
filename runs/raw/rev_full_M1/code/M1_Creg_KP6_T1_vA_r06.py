import numpy as np
import pandas as pd
from scipy import stats

# ====================== 第一部分：计算年化夏普比率 ======================
# 模拟课程数据快照 "fund" 列的日收益（假设数据）
# 这里假设有 252 个交易日的日收益数据（一年）
np.random.seed(42)  # 确保可复现
daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=252)  # 日收益均值 0.05%，标准差 1%

# 无风险利率年化 2.1%，转换为日无风险利率
annual_risk_free_rate = 0.021
daily_risk_free_rate = (1 + annual_risk_free_rate) ** (1 / 252) - 1

# 计算超额收益（日收益 - 日无风险利率）
excess_daily_returns = daily_returns - daily_risk_free_rate

# 年化夏普比率 = (年化超额收益均值) / (年化超额收益标准差)
annualized_excess_return_mean = np.mean(excess_daily_returns) * 252
annualized_excess_return_std = np.std(excess_daily_returns, ddof=1) * np.sqrt(252)
sharpe_annual = annualized_excess_return_mean / annualized_excess_return_std

# ====================== 第二部分：计算配置、选择与交互效应 ======================
# 组合与基准的权重和收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算组合和基准的总收益
portfolio_total_return = np.sum(portfolio_weights * portfolio_returns)
benchmark_total_return = np.sum(benchmark_weights * benchmark_returns)

# 配置效应（Allocation Effect）：
# Σ[(组合权重 - 基准权重) * (基准收益 - 基准总收益)]
allocation_effect = np.sum(
    (portfolio_weights - benchmark_weights) * (benchmark_returns - benchmark_total_return)
)

# 选择效应（Selection Effect）：
# Σ[(基准权重) * (组合收益 - 基准收益)]
selection_effect = np.sum(
    benchmark_weights * (portfolio_returns - benchmark_returns)
)

# 交互效应（Interaction Effect）：
# Σ[(组合权重 - 基准权重) * (组合收益 - 基准收益)]
interaction_effect = np.sum(
    (portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns)
)

# 验证：总超额收益 = 配置效应 + 选择效应 + 交互效应
total_excess_return = portfolio_total_return - benchmark_total_return
assert np.isclose(total_excess_return, allocation_effect + selection_effect + interaction_effect), "效应计算不匹配"

# ====================== 输出结果 ======================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果以供验证
print("Result Dictionary:")
print(result)

import numpy as np
import pandas as pd
from scipy import stats

# ====================== 第一部分：计算年化夏普比率 ======================
# 模拟读取课程数据快照 "fund" 列的日收益（假设数据）
np.random.seed(42)  # 确保可复现
n_days = 252  # 一年的交易日天数
daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益

# 无风险利率（年化）
risk_free_rate_annual = 0.021
risk_free_rate_daily = risk_free_rate_annual / n_days

# 计算年化夏普比率
excess_daily_returns = daily_returns - risk_free_rate_daily
sharpe_ratio_annual = np.sqrt(n_days) * excess_daily_returns.mean() / excess_daily_returns.std()

# ====================== 第二部分：计算配置、选择与交互效应 ======================
# 组合和基准的权重与收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算总收益差异
total_effect = (portfolio_weights * portfolio_returns).sum() - (benchmark_weights * benchmark_returns).sum()

# 计算配置效应（Allocation Effect）
allocation_effect = ((portfolio_weights - benchmark_weights) * benchmark_returns).sum()

# 计算选择效应（Selection Effect）
selection_effect = (benchmark_weights * (portfolio_returns - benchmark_returns)).sum()

# 计算交互效应（Interaction Effect）
interaction_effect = ((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns)).sum()

# 验证总效应 = 配置效应 + 选择效应 + 交互效应
assert np.isclose(total_effect, allocation_effect + selection_effect + interaction_effect), "效应分解不匹配"

# ====================== 结果存储 ======================
result = {
    'sharpe_annual': sharpe_ratio_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（可选，用于验证）
print(result)

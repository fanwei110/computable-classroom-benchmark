import numpy as np
import pandas as pd

# 1. 模拟读取快照CSV数据（由于没有实际CSV文件，我们直接创建数据）
# 假设fund列为基金的日收益率，rf为年化无风险利率2.1%
np.random.seed(42)  # 确保可复现
n_days = 252  # 一年的交易日数量
fund_daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益率
rf_annual = 0.021  # 年化无风险利率2.1%

# 2. 计算年化夏普比率
# 计算超额收益（减去日无风险利率）
rf_daily = (1 + rf_annual) ** (1/252) - 1  # 日无风险利率
excess_daily_returns = fund_daily_returns - rf_daily

# 年化夏普比率 = (年化超额收益均值) / (年化超额收益标准差)
annualized_excess_return = np.mean(excess_daily_returns) * 252
annualized_excess_volatility = np.std(excess_daily_returns) * np.sqrt(252)
sharpe_annual = annualized_excess_return / annualized_excess_volatility

# 3. 业绩归因分析
# 组合和基准的权重及收益数据
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算总主动收益
active_return = np.sum(portfolio_weights * portfolio_returns) - np.sum(benchmark_weights * benchmark_returns)

# 配置效应（Allocation Effect）
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * benchmark_returns)

# 选择效应（Selection Effect）
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 交互效应（Interaction Effect）
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# 验证：总主动收益 = 配置效应 + 选择效应 + 交互效应
assert np.isclose(active_return, allocation_effect + selection_effect + interaction_effect), "归因分解不匹配"

# 4. 填充result字典
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（可选，方便调试）
print(result)

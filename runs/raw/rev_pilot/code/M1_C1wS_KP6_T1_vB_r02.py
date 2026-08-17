import numpy as np
import pandas as pd

# 1. 读取快照CSV（这里模拟数据，实际使用时应替换为真实CSV读取）
# 假设CSV中有'fund_returns'列，表示基金的日收益率
# 由于题目没有提供具体CSV，我们直接使用题目给定的数据
fund_daily_returns = pd.Series([0.0005, -0.0003, 0.0012, ...])  # 示例数据，实际应从CSV读取
rf_daily = 0.021 / 252  # 年化无风险利率2.1%转换为日利率（假设252交易日）

# 计算超额收益
excess_returns = fund_daily_returns - rf_daily

# 2. 计算年化夏普比率
sharpe_ratio_daily = excess_returns.mean() / excess_returns.std()
sharpe_annual = sharpe_ratio_daily * np.sqrt(252)
result = {'sharpe_annual': sharpe_annual}

# 3. 业绩归因分析
# 题目给定的数据
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算各项效应
# 配置效应（Allocation Effect）
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * benchmark_returns)

# 选择效应（Selection Effect）
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 交互效应（Interaction Effect）
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# 4. 填充result字典
result.update({
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
})

# 输出结果（实际使用时可删除print，仅用于验证）
print(result)

import numpy as np
import pandas as pd

# 第一部分：计算年化夏普比率
# 读取数据
data_path = 'data/market_snapshot_v1.csv'
market_data = pd.read_csv(data_path)

# 提取基金日收益率
fund_returns = market_data['fund'].dropna().values

# 计算日无风险利率（年利率2.1%）
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252

# 计算超额收益率
excess_returns = fund_returns - daily_rf_rate

# 计算样本标准差（ddof=1）
daily_volatility = np.std(excess_returns, ddof=1)

# 年化夏普比率
sharpe_annual = np.mean(excess_returns) / daily_volatility * np.sqrt(252)

# 第二部分：Brinson-Hood-Beebower业绩归因
# 组合和基准的权重与收益率
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算配置效应
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * benchmark_returns)

# 计算选择效应
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 计算交互效应
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# 存储结果
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（可选，用于验证）
print(result)

import numpy as np
import pandas as pd

# 1. 读取数据并计算超额收益
def calculate_sharpe():
    # 读取CSV文件
    df = pd.read_csv('data/market_snapshot_v1.csv')

    # 提取基金日收益率（假设列名为'fund'）
    fund_returns = df['fund'].dropna().values

    # 年化无风险利率2.1%，转换为日无风险利率
    annual_rf = 0.021
    daily_rf = (1 + annual_rf) ** (1/252) - 1

    # 计算超额收益（减去无风险利率）
    excess_returns = fund_returns - daily_rf

    # 计算年化夏普比率
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

    return sharpe_ratio

# 2. 计算业绩归因效应
def calculate_attribution_effects():
    # 组合和基准的权重与收益
    portfolio_weights = np.array([0.45, 0.35, 0.20])
    benchmark_weights = np.array([0.40, 0.40, 0.20])
    portfolio_returns = np.array([0.083, 0.021, -0.014])
    benchmark_returns = np.array([0.067, 0.034, -0.009])

    # 计算总主动收益
    active_weights = portfolio_weights - benchmark_weights
    total_active_return = np.sum(portfolio_weights * portfolio_returns) - np.sum(benchmark_weights * benchmark_returns)

    # 配置效应（allocation effect）
    allocation_effect = np.sum(active_weights * benchmark_returns)

    # 选择效应（selection effect）
    selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

    # 交互效应（interaction effect）
    interaction_effect = np.sum(active_weights * (portfolio_returns - benchmark_returns))

    return allocation_effect, selection_effect, interaction_effect

# 计算结果
sharpe_annual = calculate_sharpe()
allocation_effect, selection_effect, interaction_effect = calculate_attribution_effects()

# 存储结果
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（可选，用于验证）
print(result)

import numpy as np
import pandas as pd

# ====================== 1. 读取数据并计算夏普比率 ======================
# 假设数据文件名为 'fund_returns.csv'，且包含 'fund' 列的日收益率
# 由于题目未提供实际文件，我们模拟一个典型的数据结构
# 实际使用时，请确保文件路径和格式正确
try:
    df = pd.read_csv('fund_returns.csv')  # 读取CSV文件
    daily_returns = df['fund'].dropna().values  # 提取基金日收益率
except FileNotFoundError:
    # 如果文件不存在，使用模拟数据（仅用于演示）
    np.random.seed(42)
    daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=1000)  # 模拟1000个交易日的日收益率

# 无风险利率：年化2.1%，转换为日无风险利率
annual_rf = 0.021
daily_rf = (1 + annual_rf) ** (1/252) - 1  # 假设一年252个交易日

# 计算超额收益（日收益率 - 日无风险利率）
excess_returns = daily_returns - daily_rf

# 年化夏普比率 = (年化超额收益均值) / (年化超额收益标准差)
annualized_excess_return = np.mean(excess_returns) * 252
annualized_excess_volatility = np.std(excess_returns) * np.sqrt(252)
sharpe_annual = annualized_excess_return / annualized_excess_volatility

# ====================== 2. 业绩归因分析 ======================
# 组合和基准的行业权重及收益率
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算主动权重（组合权重 - 基准权重）
active_weights = portfolio_weights - benchmark_weights

# 计算各效应
allocation_effect = np.sum(active_weights * benchmark_returns)
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))
interaction_effect = np.sum(active_weights * (portfolio_returns - benchmark_returns))

# ====================== 3. 填充结果 ======================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（可选，用于调试）
print(result)

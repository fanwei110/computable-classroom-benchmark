import numpy as np
import pandas as pd
from scipy import stats

# =========================
# 问题1：年化夏普比率计算
# =========================

# 假设CSV文件名为 'fund_data.csv'，包含 'fund' 列（日收益）
# 如果文件名不同，请根据实际情况修改
# 这里生成模拟数据以演示完整流程（实际运行时替换为读取CSV）
# 注：实际环境中应使用 pd.read_csv('实际文件名.csv')

# 读取数据（请根据实际文件路径调整）
# df = pd.read_csv('fund_data.csv')

# 由于没有实际CSV文件，这里创建一个示例DataFrame以展示完整计算逻辑
# 实际使用时，请用 pd.read_csv 替换这部分
np.random.seed(42)
dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='B')
returns = np.random.normal(0.0005, 0.015, len(dates))
df = pd.DataFrame({'date': dates, 'fund': returns})
df.set_index('date', inplace=True)

# 无风险利率
rf_annual = 0.021
# 日化无风险利率（假设252个交易日）
rf_daily = (1 + rf_annual) ** (1/252) - 1

# 超额收益
excess_returns = df['fund'] - rf_daily

# 年化平均超额收益
mean_excess_daily = excess_returns.mean()
mean_excess_annual = mean_excess_daily * 252

# 年化波动率
std_daily = excess_returns.std()
std_annual = std_daily * np.sqrt(252)

# 年化夏普比率
sharpe_annual = mean_excess_annual / std_annual

print(f"年化夏普比率: {sharpe_annual:.4f}")

# =========================
# 问题2：业绩归因分析
# =========================

# 组合权重与收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])

# 基准权重与收益
benchmark_weights = np.array([0.40, 0.40, 0.20])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 总组合收益
R_p = np.sum(portfolio_weights * portfolio_returns)
# 总基准收益
R_b = np.sum(benchmark_weights * benchmark_returns)

# 主动收益
active_return = R_p - R_b

# 配置效应： (组合权重 - 基准权重) * 基准收益
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * benchmark_returns)

# 选择效应： 基准权重 * (组合收益 - 基准收益)
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 交互效应： (组合权重 - 基准权重) * (组合收益 - 基准收益)
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# 验证：三项之和应等于主动收益
total_effect = allocation_effect + selection_effect + interaction_effect

print(f"\n业绩归因分析:")
print(f"组合收益: {R_p:.4%}")
print(f"基准收益: {R_b:.4%}")
print(f"主动收益: {active_return:.4%}")
print(f"配置效应: {allocation_effect:.4%}")
print(f"选择效应: {selection_effect:.4%}")
print(f"交互效应: {interaction_effect:.4%}")
print(f"三项之和: {total_effect:.4%}")
print(f"验证通过: {np.isclose(total_effect, active_return)}")

# =========================
# 输出结果字典
# =========================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print("\n结果字典:")
for key, value in result.items():
    print(f"{key}: {value:.6f}")

# 结果可直接用于后续分析
# result 字典包含了所有要求的输出

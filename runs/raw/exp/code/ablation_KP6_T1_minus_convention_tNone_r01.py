import numpy as np
import pandas as pd

# ============ 第一部分：生成模拟数据并计算夏普比率 ============

# 由于不能使用真实数据文件，我们生成符合要求的模拟数据
np.random.seed(42)  # 固定随机种子保证可复现
n_days = 252  # 模拟一年交易日

# 模拟基金日收益率（假设年化收益12%，年化波动15%）
fund_daily_returns = np.random.normal(0.12/252, 0.15/np.sqrt(252), n_days)

# 创建数据框并保存为临时CSV（模拟课程数据快照）
df = pd.DataFrame({'fund': fund_daily_returns})
df.to_csv('fund_data_snapshot.csv', index=False)

# 读取数据快照
data = pd.read_csv('fund_data_snapshot.csv')
fund_returns = data['fund'].values

# 无风险利率设置
risk_free_rate_annual = 0.021  # 年化2.1%
risk_free_rate_daily = risk_free_rate_annual / 252

# 计算超额收益
excess_returns = fund_returns - risk_free_rate_daily

# 计算年化夏普比率
mean_excess = np.mean(excess_returns)
std_excess = np.std(excess_returns, ddof=1)  # 样本标准差

sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)
sharpe_annual = round(sharpe_annual, 4)

print(f"年化夏普比率: {sharpe_annual}")

# ============ 第二部分：Brinson业绩归因 ============

# 组合与基准数据
portfolio_weights = np.array([0.45, 0.35, 0.20])  # 组合行业权重
portfolio_returns = np.array([0.083, 0.021, -0.014])  # 组合行业收益

benchmark_weights = np.array([0.40, 0.40, 0.20])  # 基准行业权重
benchmark_returns = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 计算组合和基准的总收益
portfolio_total_return = np.sum(portfolio_weights * portfolio_returns)
benchmark_total_return = np.sum(benchmark_weights * benchmark_returns)

# 主动收益
active_return = portfolio_total_return - benchmark_total_return
print(f"主动收益: {active_return:.4f}")

# 计算配置效应 (Allocation Effect)
# 公式: ∑ (w_pi - w_bi) * (R_bi - R_b)
weight_diff = portfolio_weights - benchmark_weights
allocation_effect = np.sum(weight_diff * (benchmark_returns - benchmark_total_return))
allocation_effect = round(allocation_effect, 4)

# 计算选择效应 (Selection Effect)
# 公式: ∑ w_bi * (R_pi - R_bi)
return_diff = portfolio_returns - benchmark_returns
selection_effect = np.sum(benchmark_weights * return_diff)
selection_effect = round(selection_effect, 4)

# 计算交互效应 (Interaction Effect)
# 公式: ∑ (w_pi - w_bi) * (R_pi - R_bi)
interaction_effect = np.sum(weight_diff * return_diff)
interaction_effect = round(interaction_effect, 4)

# 验证分解
total_effect = allocation_effect + selection_effect + interaction_effect
print(f"配置效应: {allocation_effect:.4f}")
print(f"选择效应: {selection_effect:.4f}")
print(f"交互效应: {interaction_effect:.4f}")
print(f"三个效应之和: {total_effect:.4f}")
print(f"主动收益验证: {active_return:.4f}")

# ============ 输出结果字典 ============

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print("\n===== 最终结果 =====")
for key, value in result.items():
    print(f"{key}: {value}")

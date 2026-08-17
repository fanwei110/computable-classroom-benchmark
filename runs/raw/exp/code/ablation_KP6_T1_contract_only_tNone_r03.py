import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 设置随机种子以确保可复现
np.random.seed(42)

# ==================== 第一部分：计算年化夏普比率 ====================

# 生成模拟的课程数据快照（日收益数据）
# 假设有252个交易日的数据
n_days = 252

# 生成模拟的日收益数据（假设年化收益率为12%，年化波动率为20%）
daily_mean_return = 0.12 / 252  # 日均收益率
daily_volatility = 0.20 / np.sqrt(252)  # 日波动率
daily_returns = np.random.normal(daily_mean_return, daily_volatility, n_days)

# 创建DataFrame模拟课程数据
fund_data = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=n_days, freq='B'),
    'fund': daily_returns
})

# 提取"fund"列的日收益
fund_daily_returns = fund_data['fund'].values

# 计算年化夏普比率
# 无风险利率
risk_free_rate_annual = 0.021  # 2.1%
risk_free_rate_daily = risk_free_rate_annual / 252

# 计算日超额收益
excess_daily_returns = fund_daily_returns - risk_free_rate_daily

# 计算年化夏普比率
# 年化超额收益
annual_excess_return = np.mean(excess_daily_returns) * 252

# 年化波动率
annual_volatility = np.std(fund_daily_returns, ddof=1) * np.sqrt(252)

# 夏普比率
sharpe_annual = annual_excess_return / annual_volatility

# ==================== 第二部分：Brinson分析 ====================

# 定义权重和收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
benchmark_weights = np.array([0.40, 0.40, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算配置效应 (Allocation Effect)
# 配置效应 = (组合权重 - 基准权重) * (基准收益 - 总基准收益)
total_benchmark_return = np.sum(benchmark_weights * benchmark_returns)
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * 
                          (benchmark_returns - total_benchmark_return))

# 计算选择效应 (Selection Effect)
# 选择效应 = 基准权重 * (组合收益 - 基准收益)
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 计算交互效应 (Interaction Effect)
# 交互效应 = (组合权重 - 基准权重) * (组合收益 - 基准收益)
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * 
                           (portfolio_returns - benchmark_returns))

# 验证：总超额收益 = 配置效应 + 选择效应 + 交互效应
total_excess_return = np.sum(portfolio_weights * portfolio_returns) - total_benchmark_return

# ==================== 输出结果 ====================

# 将所有结果存入字典
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print("=== 第一部分：年化夏普比率 ===")
print(f"年化夏普比率: {sharpe_annual:.4f}")
print(f"日收益率平均数: {np.mean(fund_daily_returns):.6f}")
print(f"日收益率标准差: {np.std(fund_daily_returns, ddof=1):.6f}")
print(f"年化收益率: {annual_excess_return + risk_free_rate_annual:.4f}")
print(f"年化波动率: {annual_volatility:.4f}")

print("\n=== 第二部分：Brinson分析 ===")
print(f"组合总收益: {np.sum(portfolio_weights * portfolio_returns):.4f}")
print(f"基准总收益: {total_benchmark_return:.4f}")
print(f"总超额收益: {total_excess_return:.4f}")
print(f"\n配置效应 (Allocation Effect): {allocation_effect:.4f}")
print(f"选择效应 (Selection Effect): {selection_effect:.4f}")
print(f"交互效应 (Interaction Effect): {interaction_effect:.4f}")
print(f"\n验证：配置效应 + 选择效应 + 交互效应 = {allocation_effect + selection_effect + interaction_effect:.4f}")
print(f"总超额收益 = {total_excess_return:.4f}")

# 保存结果字典
print("\n=== 结果字典 result ===")
print(result)

# 可视化Brinson分析结果
plt.figure(figsize=(10, 6))

effects = ['Allocation', 'Selection', 'Interaction']
values = [allocation_effect, selection_effect, interaction_effect]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

plt.bar(effects, values, color=colors, alpha=0.8)
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.ylabel('Effect Value')
plt.title('Brinson Performance Attribution Analysis')
plt.grid(True, alpha=0.3)

for i, v in enumerate(values):
    plt.text(i, v + 0.001 if v >= 0 else v - 0.003, f'{v:.4f}', 
             ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

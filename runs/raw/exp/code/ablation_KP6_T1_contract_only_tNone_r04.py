import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# 设置随机种子以确保可复现性
np.random.seed(42)

# 生成示例课程数据快照
# 创建模拟的基金日收益数据（250个交易日）
n_days = 250
np.random.seed(42)
daily_returns = np.random.normal(0.0005, 0.01, n_days)  # 模拟日收益

# 创建DataFrame
dates = pd.date_range(start='2023-01-01', periods=n_days, freq='B')
fund_data = pd.DataFrame({
    'fund': daily_returns
}, index=dates)

# 第一部分：计算年化夏普比率
# 计算日收益率均值
daily_mean_return = fund_data['fund'].mean()

# 计算日收益率标准差
daily_std_return = fund_data['fund'].std()

# 无风险利率（年化2.1%）
risk_free_rate_annual = 0.021

# 将无风险利率转换为日度（假设252个交易日）
risk_free_rate_daily = risk_free_rate_annual / 252

# 计算日度超额收益
daily_excess_return = daily_mean_return - risk_free_rate_daily

# 计算年化夏普比率
# 年化超额收益 = 日度超额收益 * 252
annual_excess_return = daily_excess_return * 252
# 年化波动率 = 日度标准差 * sqrt(252)
annual_volatility = daily_std_return * np.sqrt(252)
sharpe_annual = annual_excess_return / annual_volatility

# 第二部分：计算配置、选择与交互效应
# 定义组合和基准的权重与收益
portfolio_weights = np.array([0.45, 0.35, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_weights = np.array([0.40, 0.40, 0.20])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算总收益
portfolio_total_return = np.sum(portfolio_weights * portfolio_returns)
benchmark_total_return = np.sum(benchmark_weights * benchmark_returns)

# 计算配置效应 (Allocation Effect)
# 配置效应 = Σ(w_pi - w_bi) * (R_bi - R_b)
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * 
                          (benchmark_returns - benchmark_total_return))

# 计算选择效应 (Selection Effect)
# 选择效应 = Σw_bi * (R_pi - R_bi)
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 计算交互效应 (Interaction Effect)
# 交互效应 = Σ(w_pi - w_bi) * (R_pi - R_bi)
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * 
                           (portfolio_returns - benchmark_returns))

# 验证：总超额收益 = 配置效应 + 选择效应 + 交互效应
total_excess_return = portfolio_total_return - benchmark_total_return
check_sum = allocation_effect + selection_effect + interaction_effect

# 创建结果字典
result = {
    'sharpe_annual': round(float(sharpe_annual), 6),
    'allocation_effect': round(float(allocation_effect), 6),
    'selection_effect': round(float(selection_effect), 6),
    'interaction_effect': round(float(interaction_effect), 6)
}

# 输出验证信息
print("=" * 60)
print("第一部分：年化夏普比率计算")
print("=" * 60)
print(f"基金日均收益率: {daily_mean_return:.6f}")
print(f"基金日收益率标准差: {daily_std_return:.6f}")
print(f"年化无风险利率: {risk_free_rate_annual*100:.2f}%")
print(f"年化超额收益: {annual_excess_return:.6f}")
print(f"年化波动率: {annual_volatility:.6f}")
print(f"年化夏普比率: {sharpe_annual:.6f}")
print()
print("=" * 60)
print("第二部分：Brinson效应分解")
print("=" * 60)
print(f"组合总收益: {portfolio_total_return:.6f}")
print(f"基准总收益: {benchmark_total_return:.6f}")
print(f"总超额收益: {total_excess_return:.6f}")
print()
print("效应分解:")
print(f"  配置效应 (Allocation): {allocation_effect:.6f}")
print(f"  选择效应 (Selection): {selection_effect:.6f}")
print(f"  交互效应 (Interaction): {interaction_effect:.6f}")
print(f"  效应之和: {check_sum:.6f}")
print(f"  验证(应与总超额收益一致): {total_excess_return:.6f}")
print()
print("=" * 60)
print("结果字典 (result):")
print("=" * 60)
for key, value in result.items():
    print(f"  '{key}': {value}")
print()

# 可视化基金收益率分布
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.hist(fund_data['fund'], bins=30, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(daily_mean_return, color='red', linestyle='--', label=f'均值: {daily_mean_return:.4f}')
plt.axvline(0, color='green', linestyle='-', alpha=0.5, label='零收益线')
plt.title('基金日收益分布')
plt.xlabel('日收益率')
plt.ylabel('频数')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
cumulative_returns = (1 + fund_data['fund']).cumprod()
plt.plot(cumulative_returns.index, cumulative_returns.values, 'b-', linewidth=1)
plt.title('基金累计收益')
plt.xlabel('日期')
plt.ylabel('累计收益')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fund_analysis.png', dpi=100, bbox_inches='tight')
plt.close()

# 效应分解可视化
effects = ['配置效应', '选择效应', '交互效应']
values = [allocation_effect, selection_effect, interaction_effect]
colors = ['#FF9999', '#66B2FF', '#99FF99']

plt.figure(figsize=(8, 5))
bars = plt.bar(effects, values, color=colors, alpha=0.7, edgecolor='black')
plt.axhline(y=0, color='grey', linestyle='-', alpha=0.5)

# 在柱状图上添加数值标签
for bar, value in zip(bars, values):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., 
             height + 0.001 if height >= 0 else height - 0.003,
             f'{value:.4f}', 
             ha='center', va='bottom' if height >= 0 else 'top')

plt.title('Brinson效应分解')
plt.ylabel('效应值')
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('brinson_decomposition.png', dpi=100, bbox_inches='tight')
plt.close()

# 打印最终的result字典
print("\n最终结果字典:")
print(result)

import numpy as np
import pandas as pd
from typing import Dict, Any

# =============================================================================
# Part 1: 读取数据并计算年化夏普比率
# =============================================================================

# 创建一个模拟的基金日收益数据（由于不能联网，模拟课程快照数据）
# 假设 fund 列包含252个交易日的日收益数据（实际教学中，此处替换为 pd.read_csv）
np.random.seed(42)  # 确保结果可复现
n_days = 252
daily_returns = np.random.normal(0.0005, 0.01, n_days)  # 模拟日收益，均值0.05%，标准差1%

# 创建DataFrame模拟课程数据快照
df = pd.DataFrame({
    'fund': daily_returns,
    'date': pd.date_range(start='2023-01-01', periods=n_days, freq='B')
})

# 无风险利率：年化2.1%，转换为日利率
rf_annual = 0.021  # 2.1%
rf_daily = rf_annual / 252  # 日无风险利率

# 计算超额收益：基金日收益 - 日无风险利率
excess_returns = df['fund'] - rf_daily

# 计算年化夏普比率
# 夏普比率 = (平均超额收益 / 超额收益标准差) * sqrt(252)
mean_excess = excess_returns.mean()
std_excess = excess_returns.std(ddof=1)  # 样本标准差

sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)

print(f"年化夏普比率: {sharpe_annual:.4f}")

# =============================================================================
# Part 2: Brinson-Hood-Beebower 业绩归因
# =============================================================================

# 组合与基准数据
# 三个行业的权重和收益
portfolio_weights = np.array([0.45, 0.35, 0.20])   # 组合行业权重
portfolio_returns = np.array([0.083, 0.021, -0.014])  # 组合行业收益

benchmark_weights = np.array([0.40, 0.40, 0.20])    # 基准行业权重
benchmark_returns = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 计算主动收益（组合总收益 - 基准总收益）
portfolio_total_return = np.sum(portfolio_weights * portfolio_returns)
benchmark_total_return = np.sum(benchmark_weights * benchmark_returns)
active_return = portfolio_total_return - benchmark_total_return

print(f"\n组合总收益: {portfolio_total_return:.4f}")
print(f"基准总收益: {benchmark_total_return:.4f}")
print(f"主动收益: {active_return:.4f}")

# ---- Brinson-Hood-Beebower 分解 ----

# 1. 配置效应（Allocation Effect）：衡量行业权重配置的贡献
# allocation = (w_p - w_b) * (r_b - r_b_total)
allocation_effect = np.sum(
    (portfolio_weights - benchmark_weights) * 
    (benchmark_returns - benchmark_total_return)
)

# 2. 选择效应（Selection Effect）：衡量行业内选股能力的贡献
# selection = w_b * (r_p - r_b)
selection_effect = np.sum(
    benchmark_weights * (portfolio_returns - benchmark_returns)
)

# 3. 交互效应（Interaction Effect）：权重配置与选股能力的协同作用
# interaction = (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum(
    (portfolio_weights - benchmark_weights) * 
    (portfolio_returns - benchmark_returns)
)

# 验证：三项效应之和应等于主动收益
sum_effects = allocation_effect + selection_effect + interaction_effect
print(f"\n配置效应: {allocation_effect:.6f}")
print(f"选择效应: {selection_effect:.6f}")
print(f"交互效应: {interaction_effect:.6f}")
print(f"三项之和: {sum_effects:.6f} (应等于主动收益 {active_return:.6f})")
print(f"差异: {abs(sum_effects - active_return):.2e}")

# =============================================================================
# 填充 result 字典
# =============================================================================

result: Dict[str, Any] = {
    'sharpe_annual': round(sharpe_annual, 4),
    'allocation_effect': round(allocation_effect, 4),
    'selection_effect': round(selection_effect, 4),
    'interaction_effect': round(interaction_effect, 4)
}

print("\n===== 最终结果 =====")
for key, value in result.items():
    print(f"{key}: {value:.4f}")

# 额外的课堂演示：可视化业绩归因
import matplotlib.pyplot as plt

# 创建归因分解图
categories = ['配置效应\n(Allocation)', '选择效应\n(Selection)', '交互效应\n(Interaction)']
values = [allocation_effect, selection_effect, interaction_effect]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 左图：柱状图展示各效应
bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
ax1.axhline(y=0, color='black', linewidth=0.8)
ax1.set_title('Brinson-Hood-Beebower 业绩归因分解', fontsize=14, fontweight='bold')
ax1.set_ylabel('贡献度', fontsize=12)

# 在柱子上标注数值
for bar, val in zip(bars, values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., 
             height + 0.001 if height >= 0 else height - 0.003,
             f'{val:.4f}', ha='center', va='bottom' if height >= 0 else 'top', 
             fontsize=11, fontweight='bold')

# 右图：展示主动收益的构成
labels = ['配置效应', '选择效应', '交互效应']
sizes = values
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1']
explode = (0.05, 0.05, 0.05)

wedges, texts, autotexts = ax2.pie(
    [abs(v) for v in sizes], 
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors_pie,
    explode=explode,
    shadow=True
)

for text in texts:
    text.set_fontsize(11)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax2.set_title('各效应绝对贡献占比', fontsize=14, fontweight='bold')

# 添加主动收益注释
plt.figtext(0.5, 0.02, 
            f'主动收益 = {active_return:.4f}  |  夏普比率(年化) = {sharpe_annual:.4f}', 
            ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

print("\n脚本执行完毕。所有结果已存入 result 字典。")

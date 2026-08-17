import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# 设置随机种子确保可复现
np.random.seed(42)

# ==================== 第一部分：夏普比率计算 ====================
# 模拟生成课程数据快照中的基金日收益数据（252个交易日）
# 生成均值为0.08%/日，标准差为1.2%/日的日收益序列
n_days = 252
daily_returns = np.random.normal(loc=0.0008, scale=0.012, size=n_days)

# 计算日收益统计量
mean_daily_return = np.mean(daily_returns)
std_daily_return = np.std(daily_returns, ddof=1)  # 使用样本标准差

# 计算年化收益率（复利年化）
annual_return = (1 + mean_daily_return) ** 252 - 1

# 计算年化波动率
annual_volatility = std_daily_return * np.sqrt(252)

# 无风险利率（年化2.1%）
risk_free_rate_annual = 0.021

# 年化夏普比率
sharpe_annual = (annual_return - risk_free_rate_annual) / annual_volatility

# ==================== 第二部分：Brinson业绩归因 ====================
# 组合与基准数据
portfolio_weights = np.array([0.45, 0.35, 0.20])
portfolio_returns = np.array([0.083, 0.021, -0.014])
benchmark_weights = np.array([0.40, 0.40, 0.20])
benchmark_returns = np.array([0.067, 0.034, -0.009])

# 计算主动收益
active_return = np.sum(portfolio_weights * portfolio_returns) - np.sum(benchmark_weights * benchmark_returns)

# Brinson-Hood-Beebower归因（含交互项）
# 配置效应: Σ(w_p - w_b) * r_b
allocation_effect = np.sum((portfolio_weights - benchmark_weights) * benchmark_returns)

# 选择效应: Σw_b * (r_p - r_b)
selection_effect = np.sum(benchmark_weights * (portfolio_returns - benchmark_returns))

# 交互效应: Σ(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((portfolio_weights - benchmark_weights) * (portfolio_returns - benchmark_returns))

# 验证分解
total_effect = allocation_effect + selection_effect + interaction_effect
print(f"主动收益: {active_return:.6f}")
print(f"归因分解总和: {total_effect:.6f}")

# ==================== 构建结果字典 ====================
result = {
    'sharpe_annual': round(sharpe_annual, 6),
    'allocation_effect': round(allocation_effect, 6),
    'selection_effect': round(selection_effect, 6),
    'interaction_effect': round(interaction_effect, 6)
}

# 打印结果
print("\n===== 计算结果 =====")
print(f"年化夏普比率: {result['sharpe_annual']:.6f}")
print(f"配置效应: {result['allocation_effect']:.6f} ({result['allocation_effect']*100:.4f}%)")
print(f"选择效应: {result['selection_effect']:.6f} ({result['selection_effect']*100:.4f}%)")
print(f"交互效应: {result['interaction_effect']:.6f} ({result['interaction_effect']*100:.4f}%)")

# 验证归因分解
print(f"\n归因总和: {(result['allocation_effect'] + result['selection_effect'] + result['interaction_effect']):.6f}")
print(f"主动收益: {active_return:.6f}")

# ==================== 可视化 ====================
# 创建图表
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 图1：基金日收益分布
axes[0].hist(daily_returns, bins=30, alpha=0.7, color='steelblue', edgecolor='black')
axes[0].axvline(mean_daily_return, color='red', linestyle='--', linewidth=2, label=f'均值: {mean_daily_return:.4f}')
axes[0].set_title('基金日收益率分布', fontsize=12, fontweight='bold')
axes[0].set_xlabel('日收益率')
axes[0].set_ylabel('频次')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 图2：业绩归因分解
effects = ['配置效应\n(Allocation)', '选择效应\n(Selection)', '交互效应\n(Interaction)']
values = [allocation_effect, selection_effect, interaction_effect]
colors = ['#2ecc71', '#3498db', '#e74c3c']

bars = axes[1].bar(effects, values, alpha=0.8, color=colors, edgecolor='black', linewidth=1.2)

# 在柱状图上标注数值
for bar, val in zip(bars, values):
    height = bar.get_height()
    if height >= 0:
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.001,
                     f'{val:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    else:
        axes[1].text(bar.get_x() + bar.get_width()/2., height - 0.003,
                     f'{val:.4f}', ha='center', va='top', fontsize=11, fontweight='bold')

axes[1].axhline(y=0, color='black', linewidth=0.8)
axes[1].set_title('Brinson 业绩归因分解', fontsize=12, fontweight='bold')
axes[1].set_ylabel('效应值')
axes[1].grid(True, alpha=0.3, axis='y')

# 添加总和的注释
total_text = f'归因总和: {total_effect:.4f}'
axes[1].text(0.5, min(values)-0.005 if min(values) < 0 else 0.01, 
             total_text, ha='center', fontsize=10, style='italic',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

plt.tight_layout()
plt.show()

# 输出最终结果字典
print(f"\n最终结果对象: {result}")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ===== 第一部分：计算年化夏普比率 =====
# 构造课程数据快照（正常教学环境下应有真实数据，此处为示例数据）
np.random.seed(42)  # 保证可复现
n_days = 252
# 生成模拟的日收益率数据（均值0.05%/天，标准差0.8%/天）
daily_returns = np.random.normal(0.0005, 0.008, n_days)

# 无风险利率每年2.1%
rf_annual = 0.021
# 转换为日无风险利率（简单除法）
rf_daily = rf_annual / 252

# 计算超额收益
excess_returns = daily_returns - rf_daily

# 年化夏普比率 = (平均日超额收益 * 252) / (日收益率标准差 * sqrt(252))
mean_excess_daily = np.mean(excess_returns)
std_daily = np.std(daily_returns, ddof=1)  # 样本标准差

# 年化
sharpe_annual = (mean_excess_daily * 252) / (std_daily * np.sqrt(252))

print(f"第一部分 - 年化夏普比率: {sharpe_annual:.4f}")

# ===== 第二部分：Brinson-Hood-Beebower 业绩归因 =====
# 组合与基准各含三个行业
# 组合权重和收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重和收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 主动权重
w_diff = w_p - w_b

# 配置效应 = Σ(w_p - w_b) * r_b
allocation_effect = np.sum(w_diff * r_b)

# 选择效应 = Σw_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum(w_diff * (r_p - r_b))

# 验证：主动收益 = 配置 + 选择 + 交互
active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)
sum_effects = allocation_effect + selection_effect + interaction_effect

print(f"\n第二部分 - 业绩归因结果:")
print(f"配置效应 (Allocation Effect): {allocation_effect:.4f} ({allocation_effect*100:.2f}%)")
print(f"选择效应 (Selection Effect): {selection_effect:.4f} ({selection_effect*100:.2f}%)")
print(f"交互效应 (Interaction Effect): {interaction_effect:.4f} ({interaction_effect*100:.2f}%)")
print(f"\n验证: 主动收益 = {active_return:.4f} ({active_return*100:.2f}%)")
print(f"三项之和 = {sum_effects:.4f} ({sum_effects*100:.2f}%)")

# ===== 输出结果字典 =====
result = {
    'sharpe_annual': round(sharpe_annual, 6),
    'allocation_effect': round(allocation_effect, 6),
    'selection_effect': round(selection_effect, 6),
    'interaction_effect': round(interaction_effect, 6)
}

print(f"\n===== 最终结果字典 =====")
for key, value in result.items():
    print(f"{key}: {value}")

# ===== 可视化可选（对理解有帮助） =====
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左图：收益率分布
axes[0].hist(daily_returns, bins=30, color='steelblue', edgecolor='white')
axes[0].axvline(x=rf_daily, color='red', linestyle='--', label=f'无风险利率(日)={rf_daily:.6f}')
axes[0].set_title('日收益率分布', fontsize=12, fontweight='bold')
axes[0].set_xlabel('日收益率')
axes[0].set_ylabel('频数')
axes[0].legend()

# 右图：主动收益分解（业绩归因）
effects_names = ['配置效应', '选择效应', '交互效应']
effects_values = [allocation_effect, selection_effect, interaction_effect]
colors = ['#2ecc71', '#3498db', '#e74c3c']

bars = axes[1].bar(effects_names, effects_values, color=colors, width=0.5)
axes[1].axhline(y=0, color='black', linewidth=0.8)
axes[1].set_title('主动收益归因分解', fontsize=12, fontweight='bold')
axes[1].set_ylabel('贡献度')

# 在柱子上显示数值
for bar, val in zip(bars, effects_values):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., 
                 height if height > 0 else height - 0.002,
                 f'{val*100:.2f}%', 
                 ha='center', va='bottom' if height > 0 else 'top')

plt.tight_layout()
plt.show()

print("\n脚本执行完毕，所有结果已存入 result 字典。")

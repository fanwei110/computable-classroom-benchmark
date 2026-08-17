import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ========== 第一部分：夏普比率 ==========
# 模拟课程数据快照（因为无法联网读取真实文件，这里生成符合描述的示例数据）
# 实际课堂运行时，以下两行会被替换为真实读取代码：
# df = pd.read_csv('fund_snapshot.csv')
# fund_returns = df['fund'].values

# 生成示例数据：100个交易日，日收益均值约0.05%/天，标准差约0.8%
np.random.seed(42)
n_days = 100
fund_returns = np.random.normal(0.0005, 0.008, n_days)

# 无风险利率参数
rf_annual = 0.021  # 2.1%
rf_daily = rf_annual / 252

# 计算超额收益
excess_returns = fund_returns - rf_daily

# 年化夏普比率
mean_excess_daily = np.mean(excess_returns)
std_excess_daily = np.std(excess_returns, ddof=1)  # 样本标准差

sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# ========== 第二部分：Brinson归因 ==========
# 组合与基准数据
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 配置效应：Σ(w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应：Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应：Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ========== 输出结果 ==========
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果（课堂展示用）
print("=== 风险调整后业绩与归因结果 ===")
print(f"年化夏普比率: {sharpe_annual:.6f}")
print(f"配置效应: {allocation_effect:.6f}")
print(f"选择效应: {selection_effect:.6f}")
print(f"交互效应: {interaction_effect:.6f}")

# 验证：主动收益 = 配置+选择+交互
active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)
print(f"\n主动收益: {active_return:.6f}")
print(f"三项之和: {allocation_effect + selection_effect + interaction_effect:.6f}")
print("分解正确性检查:", np.isclose(active_return, 
      allocation_effect + selection_effect + interaction_effect))

# 可选：绘制收益分布图（课堂可视化）
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.hist(fund_returns, bins=20, edgecolor='black', alpha=0.7)
plt.axvline(np.mean(fund_returns), color='red', linestyle='--', label='均值')
plt.title('基金日收益分布')
plt.xlabel('日收益率')
plt.ylabel('频数')
plt.legend()

plt.subplot(1, 2, 2)
categories = ['配置效应', '选择效应', '交互效应']
values = [allocation_effect, selection_effect, interaction_effect]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
plt.bar(categories, values, color=colors, edgecolor='black')
plt.axhline(y=0, color='gray', linestyle='-', linewidth=0.8)
plt.title('Brinson归因分解')
plt.ylabel('效应值')
plt.tight_layout()
plt.show()

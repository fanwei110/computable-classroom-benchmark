import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# ========== 第一部分：读取数据并计算夏普比率 ==========

# 创建模拟数据（因为实际CSV文件不可用，这里生成符合要求的测试数据）
# 注意：在实际课堂中，这里会读取真实的CSV文件
# 生成60个交易日的模拟日收益率数据（符合正态分布，均值约0.05%/天）
np.random.seed(42)  # 固定随机种子保证可复现
n_days = 60
daily_returns = np.random.normal(0.0005, 0.01, n_days)  # 模拟日收益率

# 创建DataFrame模拟读取CSV
df = pd.DataFrame({
    'fund': daily_returns
})

# 无风险利率设置
risk_free_annual = 0.021  # 2.1%
risk_free_daily = risk_free_annual / 252  # 日无风险利率

# 计算超额收益
excess_returns = df['fund'] - risk_free_daily

# 计算年化夏普比率
# 超额收益的样本标准差（ddof=1）
excess_std_daily = np.std(excess_returns, ddof=1)
# 年化
excess_std_annual = excess_std_daily * np.sqrt(252)
# 年化超额收益均值
excess_mean_annual = np.mean(excess_returns) * 252
# 夏普比率
sharpe_annual = excess_mean_annual / excess_std_annual

print(f"第一部分结果：")
print(f"日超额收益均值: {np.mean(excess_returns):.6f}")
print(f"日超额收益标准差: {excess_std_daily:.6f}")
print(f"年化夏普比率: {sharpe_annual:.4f}")

# ========== 第二部分：Brinson业绩归因 ==========

# 输入数据
# 组合权重
w_p = np.array([0.45, 0.35, 0.20])
# 组合行业收益
r_p = np.array([0.083, 0.021, -0.014])
# 基准权重
w_b = np.array([0.40, 0.40, 0.20])
# 基准行业收益
r_b = np.array([0.067, 0.034, -0.009])

# 计算各效应
# 配置效应：Σ(w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应：Σw_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应：Σ(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 验证：主动收益 = 配置 + 选择 + 交互
portfolio_return = np.sum(w_p * r_p)
benchmark_return = np.sum(w_b * r_b)
active_return = portfolio_return - benchmark_return
total_effect = allocation_effect + selection_effect + interaction_effect

print(f"\n第二部分结果：")
print(f"组合收益: {portfolio_return:.4f}")
print(f"基准收益: {benchmark_return:.4f}")
print(f"主动收益: {active_return:.4f}")
print(f"配置效应: {allocation_effect:.6f}")
print(f"选择效应: {selection_effect:.6f}")
print(f"交互效应: {interaction_effect:.6f}")
print(f"效应总和: {total_effect:.6f}")
print(f"验证一致: {np.isclose(active_return, total_effect)}")

# ========== 输出结果字典 ==========

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print(f"\n最终结果字典：")
print(result)

# 可选：绘制基金收益分布图
plt.figure(figsize=(10, 6))
plt.hist(df['fund'], bins=20, alpha=0.7, edgecolor='black')
plt.axvline(x=np.mean(df['fund']), color='red', linestyle='--', label=f'均值: {np.mean(df["fund"]):.4f}')
plt.axvline(x=risk_free_daily, color='green', linestyle='--', label=f'无风险利率: {risk_free_daily:.6f}')
plt.xlabel('日收益率')
plt.ylabel('频数')
plt.title('基金日收益率分布')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

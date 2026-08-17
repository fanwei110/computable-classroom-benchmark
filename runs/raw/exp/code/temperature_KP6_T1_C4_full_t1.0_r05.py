import numpy as np
import pandas as pd

# ========== 第一部分：计算年化夏普比率 ==========

# 读取课程数据快照（假设 CSV 文件名为 'fund_data.csv'，包含一列 'fund' 日收益）
# 说明：由于实际文件不存在，这里创建一个模拟数据演示完整流程。
# 教师在实际课堂上请将文件路径调整为真实路径。
# 此处使用随机种子确保可复现，并用 252 个交易日模拟。
np.random.seed(42)
dates = pd.date_range(start='2024-01-01', periods=252, freq='B')
fund_returns = np.random.normal(0.0005, 0.008, size=252)  # 模拟日收益
df = pd.DataFrame({'fund': fund_returns}, index=dates)

# 无风险利率年化 2.1%（小数0.021），每日无风险利率
rf_annual = 0.021
rf_daily = rf_annual / 252

# 超额日收益
excess_daily = df['fund'] - rf_daily

# 年化夏普比率
mean_excess_daily = excess_daily.mean()
std_excess_daily = excess_daily.std(ddof=1)  # 样本标准差
sharpe_annual = mean_excess_daily / std_excess_daily * np.sqrt(252)

# ========== 第二部分：Brinson-Hood-Beebower 业绩归因 ==========

# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应：Σ (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应：Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应：Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ========== 输出结果字典 ==========

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果供课堂查看
print("=== 风险调整后业绩与归因结果 ===")
print(f"年化夏普比率: {result['sharpe_annual']:.6f}")
print(f"配置效应: {result['allocation_effect']:.6f}")
print(f"选择效应: {result['selection_effect']:.6f}")
print(f"交互效应: {result['interaction_effect']:.6f}")

# 验证：主动收益 = 配置+选择+交互
active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)
print(f"主动收益: {active_return:.6f}")
print(f"三项之和: {allocation_effect + selection_effect + interaction_effect:.6f}")

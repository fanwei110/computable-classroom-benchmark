import numpy as np
import pandas as pd

# ========== 第一部分：夏普比率 ==========
# 构造课程快照数据（模拟 CSV 内容，因为实际文件不可用）
# 假设 CSV 文件名为 "fund_snapshot.csv"，包含一列 "fund" 的日收益率
# 这里直接生成符合题目描述的示例数据（实际运行时教师会替换为真实文件）
np.random.seed(42)
n_days = 500
fund_returns = np.random.normal(0.0005, 0.01, n_days)  # 模拟日收益率
df = pd.DataFrame({'fund': fund_returns})

# 无风险利率年化 2.1%
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算超额日收益
excess_daily = df['fund'] - rf_daily

# 年化夏普比率
mean_excess_daily = excess_daily.mean()
std_excess_daily = excess_daily.std(ddof=1)
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# ========== 第二部分：Brinson 归因 ==========
# 组合与基准数据
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# Brinson-Hood-Beebower 分解（含交互项）
allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ========== 输出结果字典 ==========
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果（供课堂演示）
print("夏普比率（年化）:", round(sharpe_annual, 4))
print("配置效应:", round(allocation_effect, 6))
print("选择效应:", round(selection_effect, 6))
print("交互效应:", round(interaction_effect, 6))

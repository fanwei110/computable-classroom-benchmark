import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ==========================
# 第一部分：读取数据并计算年化夏普比率
# ==========================

# 模拟课程数据快照（“fund”列的日收益率序列）
# 这里使用正态分布随机数模拟，种子固定以保证可复现
np.random.seed(20231001)
n_days = 1000
fund_daily_returns = np.random.normal(loc=0.0008, scale=0.01, size=n_days)

# 无风险利率（年化2.1% -> 日化）
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算日超额收益
excess_daily = fund_daily_returns - rf_daily

# 年化夏普比率
mean_excess = np.mean(excess_daily)
std_excess = np.std(excess_daily, ddof=1)
sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)

# ==========================
# 第二部分：Brinson归因分析
# ==========================

# 组合与基准权重、行业收益
w_p = np.array([0.45, 0.35, 0.20])   # 组合权重
w_b = np.array([0.40, 0.40, 0.20])   # 基准权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 配置效应：Σ (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应：Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应：Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ==========================
# 输出契约
# ==========================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印详细结果（便于课堂展示）
print("=" * 40)
print("第一部分：夏普比率计算")
print(f"日收益率序列长度: {n_days} 个交易日")
print(f"年化无风险利率: {rf_annual*100:.2f}%")
print(f"日化无风险利率: {rf_daily*100:.4f}%")
print(f"日超额收益均值: {mean_excess*100:.4f}%")
print(f"日超额收益标准差: {std_excess*100:.2f}%")
print(f"年化夏普比率: {sharpe_annual:.4f}")

print("\n" + "=" * 40)
print("第二部分：Brinson-Hood-Beebower 归因")
print(f"组合权重: {w_p}")
print(f"基准权重: {w_b}")
print(f"组合行业收益: {r_p}")
print(f"基准行业收益: {r_b}")
print(f"配置效应: {allocation_effect*100:.2f}%")
print(f"选择效应: {selection_effect*100:.2f}%")
print(f"交互效应: {interaction_effect*100:.2f}%")

# 结果字典（仅用于输出契约）
result

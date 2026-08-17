import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 第一部分：计算年化夏普比率
# ------------------------------------------------------------

# 构建模拟数据（因为无法联网读取真实CSV，按题目要求生成自包含数据）
# 假设快照数据包含250个交易日，日收益率围绕0.05%均值和1%标准差生成
np.random.seed(42)  # 固定随机种子保证可复现
n_days = 250
daily_returns = np.random.normal(0.0005, 0.01, n_days)  # 日收益率序列

# 无风险利率
rf_annual = 0.021
rf_daily = rf_annual / 252

# 超额日收益率
excess_daily = daily_returns - rf_daily

# 年化夏普比率
mean_excess = excess_daily.mean()
std_excess = excess_daily.std(ddof=1)
sharpe_annual = mean_excess / std_excess * np.sqrt(252)

# ------------------------------------------------------------
# 第二部分：Brinson-Hood-Beebower 业绩归因
# ------------------------------------------------------------

# 组合与基准数据
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益

w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 配置效应：Σ (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应：Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应：Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ------------------------------------------------------------
# 输出结果字典
# ------------------------------------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果（供教师投屏展示）
print("计算结果：")
print(f"年化夏普比率：{result['sharpe_annual']:.6f}")
print(f"配置效应：{result['allocation_effect']:.6f}")
print(f"选择效应：{result['selection_effect']:.6f}")
print(f"交互效应：{result['interaction_effect']:.6f}")

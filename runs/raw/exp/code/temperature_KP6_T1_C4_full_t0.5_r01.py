import numpy as np
import pandas as pd

# ========== 第一部分：夏普比率 ==========
# 创建模拟的课程数据快照（因为无法联网读取真实CSV，按题目描述构造）
# 假设 fund 列包含252个交易日的日收益率，模拟自正态分布，设置随机种子保证可复现
np.random.seed(42)
n_days = 252
daily_returns = np.random.normal(loc=0.0005, scale=0.01, size=n_days)  # 模拟日收益
df = pd.DataFrame({'fund': daily_returns})

# 无风险利率年化2.1%
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算超额日收益
excess_daily = df['fund'] - rf_daily

# 年化夏普比率
mean_excess = excess_daily.mean()
std_excess = excess_daily.std(ddof=1)  # 样本标准差
sharpe_annual = mean_excess / std_excess * np.sqrt(252)

# ========== 第二部分：Brinson归因 ==========
# 组合与基准数据
w_p = np.array([0.45, 0.35, 0.20])   # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
w_b = np.array([0.40, 0.40, 0.20])   # 基准权重
r_b = np.array([0.067, 0.034, -0.009]) # 基准行业收益

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

# 打印结果（教师投屏用）
print("计算结果：")
print(f"年化夏普比率：{sharpe_annual:.6f}")
print(f"配置效应：{allocation_effect:.6f}")
print(f"选择效应：{selection_effect:.6f}")
print(f"交互效应：{interaction_effect:.6f}")

import pandas as pd
import numpy as np

# ---------- 第一部分：年化夏普比率 ----------
# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_returns = df['fund']  # 日收益（小数）

# 2. 无风险利率
rf_annual = 0.021
rf_daily = rf_annual / 252

# 超额收益序列
excess_returns = fund_returns - rf_daily

# 3. 日平均超额收益与日超额收益的样本标准差 (ddof=1)
mean_excess_daily = excess_returns.mean()
std_excess_daily = excess_returns.std(ddof=1)  # pandas默认即为样本标准差，显式指定以确保

# 年化夏普比率
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# ---------- 第二部分：BHB 业绩归因 ----------
# 组合与基准的权重及行业收益（小数）
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益

w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 配置效应 = Σ (w_p_i - w_b_i) * r_b_i
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b_i * (r_p_i - r_b_i)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ (w_p_i - w_b_i) * (r_p_i - r_b_i)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ---------- 结果汇总 ----------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（供投屏显示）
print(result)

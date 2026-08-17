import pandas as pd
import numpy as np

# ==================================================
# 1. 年化夏普比率计算
# ==================================================
# 读取快照CSV（请确保文件路径正确，列名包含 'fund'）
df = pd.read_csv('snapshot.csv')          # 根据实际情况修改文件名
fund_returns = df['fund'].dropna().values # 日收益序列，假设为小数形式（如0.01表示1%）

# 无风险利率参数
rf_annual = 0.021          # 年化无风险利率2.1%
trading_days = 252         # 一年交易日数
rf_daily = rf_annual / trading_days

# 日超额收益
excess_returns = fund_returns - rf_daily

# 计算年化夏普比率（样本标准差，ddof=1）
mean_excess = np.mean(excess_returns)
std_excess = np.std(excess_returns, ddof=1)
sharpe_annual = np.sqrt(trading_days) * mean_excess / std_excess

# ==================================================
# 2. 业绩归因（Brinson 模型）
# ==================================================
# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])   # 已转换为小数

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 组合与基准总收益
R_p = np.sum(w_p * r_p)
R_b = np.sum(w_b * r_b)

# 配置效应: sum_i (w_pi - w_bi) * (r_bi - R_b)
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b))

# 选择效应: sum_i w_bi * (r_pi - r_bi)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应: sum_i (w_pi - w_bi) * (r_pi - r_bi)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ==================================================
# 3. 输出结果
# ==================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 投屏展示
print(result)

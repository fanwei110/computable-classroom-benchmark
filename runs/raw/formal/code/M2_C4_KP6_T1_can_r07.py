import numpy as np
import pandas as pd

# ========================
# 第一部分：夏普比率计算
# ========================
# 读取日收益数据
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_returns = df['fund'].dropna().values  # 确保无缺失

# 无风险利率（年化2.1%）
rf_annual = 0.021
rf_daily = rf_annual / 252.0               # 简单除法换算为日利率

# 超额收益
excess_returns = fund_returns - rf_daily

# 样本统计量
mean_excess = np.mean(excess_returns)
std_excess = np.std(excess_returns, ddof=1)   # 样本标准差

# 年化夏普比率（日频 -> 年化，波动率缩放 sqrt(252)）
sharpe_annual = np.sqrt(252) * mean_excess / std_excess

# ========================
# 第二部分：Brinson‑Hood‑Beebower 业绩归因
# ========================
# 组合数据
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准数据
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应 = Σ(w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ========================
# 按契约输出结果字典
# ========================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 课堂投屏时可直接查看（不影响后续使用）
print(result)

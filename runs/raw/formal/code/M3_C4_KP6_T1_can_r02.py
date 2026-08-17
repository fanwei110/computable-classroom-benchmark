import numpy as np
import pandas as pd

# ==========================================
# 第一部分：计算年化夏普比率
# ==========================================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益
daily_returns = df['fund']

# 无风险利率参数（年化 2.1%，用小数表示）
rf_annual = 0.021

# 日无风险利率（按课程约定：年利率 / 252）
rf_daily = rf_annual / 252

# 计算日超额收益
excess_daily_returns = daily_returns - rf_daily

# 计算日超额收益的均值和样本标准差 (ddof=1)
mean_excess_daily = np.mean(excess_daily_returns)
std_excess_daily = np.std(excess_daily_returns, ddof=1)

# 计算日夏普比率并年化（按 sqrt(252) 缩放）
sharpe_daily = mean_excess_daily / std_excess_daily
sharpe_annual = sharpe_daily * np.sqrt(252)


# ==========================================
# 第二部分：Brinson-Hood-Beebower 业绩归因
# ==========================================

# 组合与基准的权重与收益（小数表示）
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应 = Σ(w_p − w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b * (r_p − r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ(w_p − w_b) * (r_p − r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==========================================
# 输出契约：填充 result 字典
# ==========================================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果以便课堂投屏展示
print(result)

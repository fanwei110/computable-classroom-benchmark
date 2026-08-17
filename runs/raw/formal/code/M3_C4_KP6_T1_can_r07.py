import pandas as pd
import numpy as np

# ==================== 第一部分：计算年化夏普比率 ====================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 获取基金日收益并确保无缺失值
fund_returns = df['fund'].dropna()

# 2. 无风险利率处理
rf_annual = 0.021  # 年利率 2.1%
rf_daily = rf_annual / 252  # 日无风险利率

# 计算日超额收益
excess_returns = fund_returns - rf_daily

# 计算超额收益的均值和样本标准差（ddof=1）
mean_excess = excess_returns.mean()
std_excess = excess_returns.std(ddof=1)

# 计算日夏普比率并年化
sharpe_daily = mean_excess / std_excess
sharpe_annual = sharpe_daily * np.sqrt(252)


# ==================== 第二部分：Brinson-Hood-Beebower 业绩归因 ====================

# 组合与基准数据
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 3. 计算配置、选择与交互效应
allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==================== 输出契约 ====================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 投屏展示结果
print(result)

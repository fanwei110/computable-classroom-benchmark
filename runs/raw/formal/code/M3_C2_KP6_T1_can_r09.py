import numpy as np
import pandas as pd

# ==================== 第一部分：计算年化夏普比率 ====================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_returns = df['fund'].values

# 题目设定：无风险利率每年 2.1%
rf_annual = 0.021

# 假设：一年按 252 个交易日计算，日无风险利率采用简单年化折算（业界常用标准）
rf_daily = rf_annual / 252

# 在基金收益中计入无风险利率，即计算日超额收益
excess_returns = fund_returns - rf_daily

# 计算日超额收益的均值与样本标准差（ddof=1 符合统计无偏估计惯例）
mean_excess_daily = np.mean(excess_returns)
std_excess_daily = np.std(excess_returns, ddof=1)

# 计算年化夏普比率：日均超额收益 / 日标准差 * sqrt(252)
sharpe_daily = mean_excess_daily / std_excess_daily
sharpe_annual = sharpe_daily * np.sqrt(252)


# ==================== 第二部分：业绩归因 (Brinson-Hood-Beebower 模型) ====================

# 组合与基准的权重及收益
wp = np.array([0.45, 0.35, 0.20])  # 组合权重
wb = np.array([0.40, 0.40, 0.20])  # 基准权重
rp = np.array([0.083, 0.021, -0.014])  # 组合行业收益
rb = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 配置效应 (Allocation Effect): 权重差异 × 基准收益
# 衡量因偏离基准权重而产生的收益
allocation_effect = np.sum((wp - wb) * rb)

# 选择效应 (Selection Effect): 基准权重 × 收益差异
# 衡量在基准权重下，因个股/行业选择优于基准而产生的收益
selection_effect = np.sum(wb * (rp - rb))

# 交互效应 (Interaction Effect): 权重差异 × 收益差异
# 衡量权重偏离与收益偏离共同作用产生的额外收益
interaction_effect = np.sum((wp - wb) * (rp - rb))

# ==================== 填充输出契约 ====================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 教师投屏展示辅助打印
print("=== 风险调整后业绩与归因分析结果 ===")
for key, value in result.items():
    print(f"{key}: {value:.6f}")

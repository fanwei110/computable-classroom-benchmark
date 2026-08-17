import pandas as pd
import numpy as np

# ================= 第一部分：读取数据并计算年化夏普比率 =================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 假设：一年包含252个交易日，日无风险利率采用单利拆分（金融计算常用简化方式）
trading_days = 252
rf_annual = 0.021

# 提取基金日收益
fund_daily_returns = df['fund']

# 计算日无风险利率
rf_daily = rf_annual / trading_days

# 在基金收益中计入无风险利率，计算日超额收益
excess_daily_returns = fund_daily_returns - rf_daily

# 计算日超额收益的均值与样本标准差（ddof=1符合金融统计惯例）
mean_excess_daily = np.mean(excess_daily_returns)
std_excess_daily = np.std(excess_daily_returns, ddof=1)

# 2. 计算年化夏普比率 (Sharpe_annual = (均值/标准差) * sqrt(252))
# 引入微小常数防止除零，保证代码健壮性
epsilon = 1e-10
sharpe_annual = (mean_excess_daily / (std_excess_daily + epsilon)) * np.sqrt(trading_days)


# ================= 第二部分：业绩归因 (Brinson-Hood-Beebower 模型) =================

# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 计算基准总收益
R_b = np.sum(w_b * r_b)

# 3. 计算配置、选择、交互效应
# 配置效应 (Allocation Effect): 衡量因权重偏离基准带来的超额收益
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b))

# 选择效应 (Selection Effect): 衡量因行业收益优于基准带来的超额收益
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect): 衡量权重偏离与收益偏离共同作用带来的超额收益
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ================= 输出契约 =================

# 4. 填充 result
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

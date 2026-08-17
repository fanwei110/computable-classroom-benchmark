import pandas as pd
import numpy as np

# ============================================================
# Part 1: 年化夏普比率 (Annualized Sharpe Ratio)
# ============================================================

# 读取数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益
fund_daily_returns = df['fund']

# 无风险利率参数
rf_annual = 0.021          # 年化无风险利率 2.1%
trading_days = 252         # 一年交易日数
rf_daily = rf_annual / trading_days  # 日化无风险利率（简单除法）

# 计算日超额收益（在基金收益中计入无风险利率）
daily_excess_returns = fund_daily_returns - rf_daily

# 年化夏普比率 = mean(日超额收益) / std(日收益) * sqrt(252)
mean_excess = daily_excess_returns.mean()
std_daily = fund_daily_returns.std(ddof=1)  # 样本标准差
sharpe_annual = mean_excess / std_daily * np.sqrt(trading_days)

# ============================================================
# Part 2: 业绩归因 (Performance Attribution - Brinson Model)
# ============================================================

# 组合与基准数据
wp = np.array([0.45, 0.35, 0.20])        # 组合权重
Rp = np.array([0.083, 0.021, -0.014])    # 组合各行业收益
wb = np.array([0.40, 0.40, 0.20])        # 基准权重
Rb = np.array([0.067, 0.034, -0.009])    # 基准各行业收益

# 配置效应 (Allocation Effect): Σ(w_p - w_b) × R_b
allocation_effect = np.sum((wp - wb) * Rb)

# 选择效应 (Selection Effect): Σ w_b × (R_p - R_b)
selection_effect = np.sum(wb * (Rp - Rb))

# 交互效应 (Interaction Effect): Σ(w_p - w_b) × (R_p - R_b)
interaction_effect = np.sum((wp - wb) * (Rp - Rb))

# ============================================================
# 验证：主动收益 = 配置 + 选择 + 交互
# ============================================================
portfolio_return = np.sum(wp * Rp)
benchmark_return = np.sum(wb * Rb)
active_return = portfolio_return - benchmark_return
assert abs(active_return - (allocation_effect + selection_effect + interaction_effect)) < 1e-10, \
    "Brinson分解不一致"

# ============================================================
# 结果输出
# ============================================================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

print(result)

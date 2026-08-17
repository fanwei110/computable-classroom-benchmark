import numpy as np
import pandas as pd

# ============================================================
# 第一部分：读取数据并计算年化夏普比率
# ============================================================

# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益序列
fund_daily_returns = df['fund'].values

# 无风险利率参数
rf_annual = 0.021          # 年化无风险利率
trading_days = 252         # 一年交易日数
rf_daily = rf_annual / trading_days  # 日无风险利率

# 计算日超额收益：基金日收益 - 日无风险利率
excess_daily_returns = fund_daily_returns - rf_daily

# 年化夏普比率 = (日超额收益均值 / 日收益标准差) × sqrt(252)
# 标准定义：分母用组合收益的标准差（总风险）
daily_mean_excess = np.mean(excess_daily_returns)
daily_std = np.std(fund_daily_returns, ddof=1)  # 样本标准差

sharpe_annual = (daily_mean_excess / daily_std) * np.sqrt(trading_days)

# ============================================================
# 第二部分：Brinson业绩归因（配置、选择、交互效应）
# ============================================================

# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
R_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
R_b = np.array([0.067, 0.034, -0.009])

# 权重差异与收益差异
delta_w = w_p - w_b   # 权重偏离
delta_R = R_p - R_b   # 收益偏离（选择能力体现）

# 配置效应：因权重偏离基准而产生的超额收益
# Allocation = Σ (w_p - w_b) × R_b
allocation_effect = np.sum(delta_w * R_b)

# 选择效应：因在行业内选股能力而产生的超额收益
# Selection = Σ w_b × (R_p - R_b)
selection_effect = np.sum(w_b * delta_R)

# 交互效应：权重偏离与收益偏离的交叉影响
# Interaction = Σ (w_p - w_b) × (R_p - R_b)
interaction_effect = np.sum(delta_w * delta_R)

# ============================================================
# 验证：主动收益 = 配置 + 选择 + 交互
# ============================================================
portfolio_return = np.sum(w_p * R_p)
benchmark_return = np.sum(w_b * R_b)
active_return = portfolio_return - benchmark_return
attrib_sum = allocation_effect + selection_effect + interaction_effect

print("=" * 55)
print("《证券投资学》—— 风险调整后业绩与业绩归因")
print("=" * 55)
print(f"\n【第一部分：年化夏普比率】")
print(f"  日收益均值:       {np.mean(fund_daily_returns):.6f}")
print(f"  日超额收益均值:   {daily_mean_excess:.6f}")
print(f"  日收益标准差:     {daily_std:.6f}")
print(f"  年化夏普比率:     {sharpe_annual:.4f}")

print(f"\n【第二部分：Brinson业绩归因】")
print(f"  组合收益:         {portfolio_return:.4f}")
print(f"  基准收益:         {benchmark_return:.4f}")
print(f"  主动收益:         {active_return:.4f}")
print(f"  ─────────────────────────────")
print(f"  配置效应:         {allocation_effect:.6f}")
print(f"  选择效应:         {selection_effect:.6f}")
print(f"  交互效应:         {interaction_effect:.6f}")
print(f"  ─────────────────────────────")
print(f"  归因合计:         {attrib_sum:.6f}")
print(f"  验证(主动-归因):  {abs(active_return - attrib_sum):.2e}")
print("=" * 55)

# ============================================================
# 输出契约：填充 result 字典
# ============================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

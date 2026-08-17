import numpy as np
import pandas as pd

# =============================================
# Part 1: 年化夏普比率
# =============================================

# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_daily_returns = df['fund']

# 无风险利率（年化）
rf_annual = 0.021

# 将年化无风险利率转换为日频（精确复利）
trading_days = 252
rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1

# 在基金收益中计入无风险利率，计算日超额收益
excess_returns = fund_daily_returns - rf_daily

# 日超额收益的均值与标准差（样本标准差 ddof=1）
mean_daily_excess = excess_returns.mean()
std_daily_excess = excess_returns.std(ddof=1)

# 年化夏普比率 = sqrt(252) × (日均超额收益 / 日超额收益标准差)
sharpe_annual = np.sqrt(trading_days) * (mean_daily_excess / std_daily_excess)

# =============================================
# Part 2: Brinson 业绩归因（Brinson-Fachler 模型）
# =============================================

# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 组合总收益与基准总收益
R_p_total = np.sum(w_p * r_p)
R_b_total = np.sum(w_b * r_b)

# --- 配置效应 (Allocation Effect) ---
# Brinson-Fachler: 超配/低配权重 × 该行业基准收益与基准总收益之差
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b_total))

# --- 选择效应 (Selection Effect) ---
# 基准权重 × 行业超额收益（组合行业收益 - 基准行业收益）
selection_effect = np.sum(w_b * (r_p - r_b))

# --- 交互效应 (Interaction Effect) ---
# 权重偏离 × 行业超额收益
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# =============================================
# 验证：三效应之和应等于主动收益
# =============================================
active_return = R_p_total - R_b_total
total_attribution = allocation_effect + selection_effect + interaction_effect
assert np.isclose(active_return, total_attribution), \
    f"归因分解不闭合: 主动收益={active_return:.6f}, 三效应之和={total_attribution:.6f}"

# =============================================
# 输出结果
# =============================================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果供课堂展示
print("=" * 55)
print("《证券投资学》—— 风险调整后业绩与业绩归因")
print("=" * 55)
print(f"\n【第一部分：年化夏普比率】")
print(f"  无风险利率（年化）: {rf_annual:.1%}")
print(f"  日均超额收益:       {mean_daily_excess:.6f}")
print(f"  日超额收益标准差:   {std_daily_excess:.6f}")
print(f"  年化夏普比率:       {sharpe_annual:.4f}")

print(f"\n【第二部分：Brinson 业绩归因】")
print(f"  组合总收益:   {R_p_total:.4f}")
print(f"  基准总收益:   {R_b_total:.4f}")
print(f"  主动收益:     {active_return:.4f}")
print(f"  ─────────────────────────")
print(f"  配置效应:     {allocation_effect:+.4f}")
print(f"  选择效应:     {selection_effect:+.4f}")
print(f"  交互效应:     {interaction_effect:+.4f}")
print(f"  ─────────────────────────")
print(f"  三效应合计:   {total_attribution:+.4f}")
print("=" * 55)

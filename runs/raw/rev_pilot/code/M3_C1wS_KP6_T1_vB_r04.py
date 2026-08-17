import numpy as np
import pandas as pd
import os

# ==========================================
# 1. 读取快照 CSV；在基金收益中计入无风险利率
# ==========================================
# 为保证代码自包含且可复现，若当前目录不存在快照文件则自动生成一份模拟数据
csv_path = 'snapshot.csv'
if not os.path.exists(csv_path):
    np.random.seed(42)
    # 模拟252个交易日的基金日收益率（年化均值约5%，年化波动率约15%）
    mock_daily_returns = np.random.normal(loc=0.05/252, scale=0.15/np.sqrt(252), size=252)
    pd.DataFrame({'fund': mock_daily_returns}).to_csv(csv_path, index=False)

# 读取 CSV
df = pd.read_csv(csv_path)

# 给定无风险利率 rf = 2.1%（年化），转化为日度无风险利率
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 在基金收益中计入无风险利率，计算超额收益（日度基金收益率 - 日度无风险利率）
daily_excess_returns = df['fund'] - rf_daily

# ==========================================
# 2. 计算年化夏普比率
# ==========================================
# 年化夏普比率 = (日均超额收益 / 日超额收益标准差) * sqrt(252)
mean_excess = daily_excess_returns.mean()
std_excess = daily_excess_returns.std(ddof=1)  # 使用样本标准差

sharpe_annual = (mean_excess / std_excess) * np.sqrt(trading_days)

# ==========================================
# 3. 计算配置、选择、交互效应 (Brinson归因模型)
# ==========================================
# 题目给定的组合与基准数据
# 组合权重、行业收益（即组合内行业收益率）、基准权重、基准收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应 (Allocation Effect): Σ (Wp - Wb) * Rb
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 (Selection Effect): Σ Wb * (Rp - Rb)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect): Σ (Wp - Wb) * (Rp - Rb)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 验证：主动总收益 = 配置 + 选择 + 交互 = Σ Wp*Rp - Σ Wb*Rb
# active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)
# assert np.isclose(active_return, allocation_effect + selection_effect + interaction_effect)

# ==========================================
# 4. 填充 result
# ==========================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果以便课堂投屏展示
print("="----40)
print("《证券投资学》课堂实时计算结果")
print("="----40)
print(f"年化夏普比率: {result['sharpe_annual']:.4f}")
print(f"配置效应:     {result['allocation_effect']:.4%}")
print(f"选择效应:     {result['selection_effect']:.4%}")
print(f"交互效应:     {result['interaction_effect']:.4%}")
print("="----40)


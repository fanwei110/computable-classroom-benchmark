import numpy as np
import pandas as pd

# ===========================
# 第一部分：年化夏普比率计算
# ===========================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益率
fund_daily_returns = df['fund'].values

# 假设处理：
# - 一年按252个交易日计算
# - 日无风险利率采用年化无风险利率除以252进行折算
# - 标准差采用样本标准差（ddof=1）
trading_days = 252
rf_annual = 0.021
rf_daily = rf_annual / trading_days

# 2. 在基金收益中计入无风险利率，计算日超额收益
excess_daily_returns = fund_daily_returns - rf_daily

# 计算日夏普比率
mean_excess = np.mean(excess_daily_returns)
std_excess = np.std(excess_daily_returns, ddof=1)

sharpe_daily = mean_excess / std_excess

# 年化夏普比率
sharpe_annual = sharpe_daily * np.sqrt(trading_days)


# ===========================
# 第二部分：业绩归因（BHB模型）
# ===========================

# 组合与基准数据
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益

w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 3. 计算配置、选择与交互效应
# 配置效应 (Allocation Effect) = sum((W_p - W_b) * R_b)
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 (Selection Effect) = sum(W_b * (R_p - R_b))
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect) = sum((W_p - W_b) * (R_p - R_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ===========================
# 存储结果
# ===========================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 课堂投屏展示输出（便于验证）
print(f"年化夏普比率: {result['sharpe_annual']:.4f}")
print(f"配置效应: {result['allocation_effect']:.4f}")
print(f"选择效应: {result['selection_effect']:.4f}")
print(f"交互效应: {result['interaction_effect']:.4f}")

# 验证：主动收益 = 配置 + 选择 + 交互
active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)
attrib_sum = allocation_effect + selection_effect + interaction_effect
print(f"\n[验证] 主动收益: {active_return:.4f}, 归因效应之和: {attrib_sum:.4f} (二者应相等)")

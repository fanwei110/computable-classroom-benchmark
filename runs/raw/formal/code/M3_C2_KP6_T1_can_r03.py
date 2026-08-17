import pandas as pd
import numpy as np

# ==========================================
# 第一部分：计算年化夏普比率
# ==========================================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益
daily_returns = df['fund']

# 假设：
# - 一年有252个交易日（业界计算年化夏普比率的通用标准）
# - 日无风险利率 = 年无风险利率 / 252 （简单算术折算）
trading_days = 252
rf_annual = 0.021
rf_daily = rf_annual / trading_days

# 2. 计算超额收益及年化夏普比率
excess_daily_returns = daily_returns - rf_daily

# 计算日超额收益的均值与标准差（使用ddof=1计算样本标准差）
mean_excess_daily = np.mean(excess_daily_returns)
std_excess_daily = np.std(excess_daily_returns, ddof=1)

# 年化夏普比率 = (日均值 / 日标准差) * sqrt(252)
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(trading_days)


# ==========================================
# 第二部分：业绩归因（配置、选择与交互效应）
# ==========================================

# 组合与基准权重及收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 3. 计算 BHB 模型三大效应
# 配置效应 (Allocation Effect) = sum( (w_p - w_b) * r_b )
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 (Selection Effect) = sum( w_b * (r_p - r_b) )
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect) = sum( (w_p - w_b) * (r_p - r_b) )
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 验证（教学演示用，确保主动收益 = 三效应之和）：
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

# 课堂投屏打印，便于直观查看
print("="*40)
print("风险调整后业绩与业绩归因计算结果：")
print("="*40)
for key, value in result.items():
    print(f"{key}: {value:.6f}")
print("="*40)

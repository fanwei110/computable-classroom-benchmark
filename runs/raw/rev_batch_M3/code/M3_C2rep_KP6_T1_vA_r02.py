import pandas as pd
import numpy as np

# ====================
# 第一部分：年化夏普比率
# ====================

# 1. 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')
daily_returns = df['fund']

# 假设：一年有252个交易日，无风险利率采用简单日化（常见且内部一致的处理方式）
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 2. 在基金收益中计入无风险利率，计算日超额收益
excess_daily_returns = daily_returns - rf_daily

# 计算日超额收益的均值与样本标准差（ddof=1 符合金融计算惯例）
mean_excess_daily = np.mean(excess_daily_returns)
std_excess_daily = np.std(excess_daily_returns, ddof=1)

# 计算年化夏普比率：日夏普 * sqrt(252)
sharpe_daily = mean_excess_daily / std_excess_daily
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# ====================
# 第二部分：业绩归因 (BHB模型)
# ====================

# 组合权重与行业收益
W_p = np.array([0.45, 0.35, 0.20])
R_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
W_b = np.array([0.40, 0.40, 0.20])
R_b = np.array([0.067, 0.034, -0.009])

# 权重差与收益差
delta_W = W_p - W_b
delta_R = R_p - R_b

# 3. 计算配置、选择与交互效应
# 配置效应 = sum(权重差 * 基准收益)
allocation_effect = np.sum(delta_W * R_b)

# 选择效应 = sum(基准权重 * 收益差)
selection_effect = np.sum(W_b * delta_R)

# 交互效应 = sum(权重差 * 收益差)
interaction_effect = np.sum(delta_W * delta_R)

# ====================
# 输出契约
# ====================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 投屏展示结果
print(result)

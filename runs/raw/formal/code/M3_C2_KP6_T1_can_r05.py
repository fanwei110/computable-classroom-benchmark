import pandas as pd
import numpy as np

# ==================== Part 1: 读取数据与无风险利率处理 ====================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 清理列名中可能存在的首尾空格，增强代码鲁棒性
df.columns = df.columns.str.strip()

# 提取 "fund" 列的日收益率，并剔除缺失值以保证计算正确
fund_daily_returns = df['fund'].dropna().values

# 假设：每年有 252 个交易日
trading_days = 252
rf_annual = 0.021

# 假设：日无风险利率采用单利折算（金融计算常用且简明的方式）
rf_daily = rf_annual / trading_days

# 在基金日收益中计入无风险利率，计算日超额收益（总收益 - 无风险收益）
daily_excess_returns = fund_daily_returns - rf_daily

# ==================== Part 2: 计算年化夏普比率 ====================
# 计算日超额收益的均值与样本标准差（ddof=1 为样本标准差，符合统计规范）
mean_excess_return = np.mean(daily_excess_returns)
std_excess_return = np.std(daily_excess_returns, ddof=1)

# 夏普比率年化公式：Sharpe_annual = (日均值 / 日标准差) * sqrt(252)
sharpe_annual = (mean_excess_return / std_excess_return) * np.sqrt(trading_days)

# ==================== Part 3：业绩归因（配置、选择与交互效应） ====================
# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应 (Allocation Effect): Σ(组合权重 - 基准权重) × 基准收益
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 (Selection Effect): Σ基准权重 × (组合收益 - 基准收益)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 (Interaction Effect): Σ(组合权重 - 基准权重) × (组合收益 - 基准收益)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ==================== Part 4：按要求格式输出结果 ====================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 课堂投屏展示结果
print(result)

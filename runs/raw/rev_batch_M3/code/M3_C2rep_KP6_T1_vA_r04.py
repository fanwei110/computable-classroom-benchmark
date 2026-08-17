import pandas as pd
import numpy as np

# ==================== 第一部分：读取数据与年化夏普比率计算 ====================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益率序列
fund_daily_returns = df['fund']

# 无风险利率处理：年化2.1%，按每年252个交易日转换为日无风险利率
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 在基金收益中计入无风险利率，计算日超额收益
excess_daily_returns = fund_daily_returns - rf_daily

# 计算年化夏普比率
# 年化超额收益均值 = 日超额收益均值 * 252
# 年化超额收益标准差 = 日超额收益标准差 * sqrt(252)
# 年化夏普比率 = 年化超额收益均值 / 年化超额收益标准差
mean_excess_daily = excess_daily_returns.mean()
std_excess_daily = excess_daily_returns.std(ddof=1) # 使用样本标准差

sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(trading_days)

# ==================== 第二部分：Brinson业绩归因计算 ====================

# 给定权重与收益数据
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014]) # 组合行业收益

w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009]) # 基准行业收益

# 计算基准总收益 R_b
R_b_total = np.sum(w_b * r_b)

# 1. 配置效应 (Allocation Effect)
# A = sum( (W_p - W_b) * (R_b - R_b_total) )
allocation_effect = np.sum((w_p - w_b) * (r_b - R_b_total))

# 2. 选择效应 (Selection Effect)
# S = sum( W_b * (R_p - R_b) )
selection_effect = np.sum(w_b * (r_p - r_b))

# 3. 交互效应 (Interaction Effect)
# I = sum( (W_p - W_b) * (R_p - R_b) )
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ==================== 第三部分：填充结果 ====================

result = {
    'sharpe_annual': float(sharpe_annual),
    'allocation_effect': float(allocation_effect),
    'selection_effect': float(selection_effect),
    'interaction_effect': float(interaction_effect)
}

# 验证输出（可在此处打印检查，最终以result字典为准）
# print(result)

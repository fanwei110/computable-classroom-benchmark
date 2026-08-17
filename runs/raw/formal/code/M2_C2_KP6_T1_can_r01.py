import pandas as pd
import numpy as np

# ============================================================
# 1. 读取数据并计算年化夏普比率
# ============================================================
# 假设数据文件位于 data/market_snapshot_v1.csv，包含列 "fund"
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益率
fund_returns = df['fund'].values  # 日简单收益率（假设为小数形式）

# 无风险利率设定
rf_annual = 0.021
trading_days = 252  # 年交易日数
rf_daily = rf_annual / trading_days

# 超额日收益率
excess_daily = fund_returns - rf_daily

# 日平均超额收益与日波动率
mean_daily_excess = np.mean(excess_daily)
std_daily_excess = np.std(excess_daily, ddof=1)  # 样本标准差

# 年化
annualized_excess_return = mean_daily_excess * trading_days
annualized_volatility = std_daily_excess * np.sqrt(trading_days)

# 年化夏普比率
sharpe_annual = annualized_excess_return / annualized_volatility

# ============================================================
# 2. 业绩归因：配置效应、选择效应、交互效应
# ============================================================
# 组合数据
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准数据
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# Brinson 归因
allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ============================================================
# 3. 输出结果
# ============================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 可选打印，便于实时查看（教师投屏）
print("年化夏普比率：", sharpe_annual)
print("配置效应：", allocation_effect)
print("选择效应：", selection_effect)
print("交互效应：", interaction_effect)

import numpy as np
import pandas as pd

# ========================
# 1. 读取数据并计算年化夏普比率
# ========================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_daily = df['fund']  # 基金日收益率（小数形式）

# 无风险利率设定（年化 2.1%），转为日度
rf_annual = 0.021
rf_daily = rf_annual / 252  # 假设一年252个交易日

# 超额日收益
excess_daily = fund_daily - rf_daily

# 日夏普比率
daily_sharpe = excess_daily.mean() / excess_daily.std()
# 年化夏普比率
sharpe_annual = daily_sharpe * np.sqrt(252)

# ========================
# 2. 业绩归因（Brinson模型）
# ========================
# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应：以基准收益衡量权重偏离
allocation_effect = float(np.sum((w_p - w_b) * r_b))
# 选择效应：以基准权重衡量个股（行业）选择能力
selection_effect = float(np.sum(w_b * (r_p - r_b)))
# 交互效应：权重偏离与选择能力的交叉项
interaction_effect = float(np.sum((w_p - w_b) * (r_p - r_b)))

# ========================
# 3. 组装结果字典
# ========================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出（供课堂投屏）
print(result)

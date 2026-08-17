import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. 读取 CSV 并计算年化夏普比率
# ------------------------------------------------------------
# 注意：课程数据快照必须存在于 data/market_snapshot_v1.csv
df = pd.read_csv('data/market_snapshot_v1.csv')

# 取基金日收益，假设为小数形式（例如 0.01 代表 1%），并剔除缺失值
fund_returns = df['fund'].dropna().values

# 无风险利率设定
rf_annual = 0.021
rf_daily = rf_annual / 252  # 一年按 252 个交易日

# 日超额收益
excess_returns = fund_returns - rf_daily

# 年化夏普比率 = sqrt(252) * (日均超额收益 / 日超额收益标准差)
# 使用样本标准差 (ddof=1) 作为波动率的无偏估计
mean_excess_daily = np.mean(excess_returns)
std_excess_daily = np.std(excess_returns, ddof=1)

sharpe_annual = np.sqrt(252) * mean_excess_daily / std_excess_daily

# ------------------------------------------------------------
# 2. 业绩归因：配置效应、选择效应、交互效应
# ------------------------------------------------------------
# 组合
wP = np.array([0.45, 0.35, 0.20])
rP = np.array([0.083, 0.021, -0.014])

# 基准
wB = np.array([0.40, 0.40, 0.20])
rB = np.array([0.067, 0.034, -0.009])

# 配置效应：Σ (wP_i - wB_i) * rB_i
allocation_effect = np.sum((wP - wB) * rB)

# 选择效应：Σ wB_i * (rP_i - rB_i)
selection_effect = np.sum(wB * (rP - rB))

# 交互效应：Σ (wP_i - wB_i) * (rP_i - rB_i)
interaction_effect = np.sum((wP - wB) * (rP - rB))

# ------------------------------------------------------------
# 3. 按要求组装结果字典
# ------------------------------------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出给教师投屏查看
print(result)

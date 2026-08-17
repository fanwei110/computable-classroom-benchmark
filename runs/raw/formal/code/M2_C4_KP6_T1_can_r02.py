import numpy as np
import pandas as pd

# ------------------------------
# 1. 读取数据并计算日超额收益
# ------------------------------
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_returns = df['fund'].values          # 基金日收益（小数）

rf_annual = 0.021                         # 年化无风险利率
rf_daily = rf_annual / 252                # 日无风险利率（简単除法）

excess_returns = fund_returns - rf_daily  # 日超额收益

# ------------------------------
# 2. 年化夏普比率
#    样本标准差 ddof=1，波动率年化 sqrt(252)
# ------------------------------
mean_excess_daily = np.mean(excess_returns)
std_excess_daily = np.std(excess_returns, ddof=1)

sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# ------------------------------
# 3. Brinson-Hood-Beebower 业绩归因
#    配置、选择、交互效应
# ------------------------------
w_p = np.array([0.45, 0.35, 0.20])   # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
w_b = np.array([0.40, 0.40, 0.20])   # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

allocation_effect  = np.sum((w_p - w_b) * r_b)
selection_effect   = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ------------------------------
# 4. 存入结果字典
# ------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 课堂展示时可直接查看
print(result)

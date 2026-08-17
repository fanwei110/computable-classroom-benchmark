import numpy as np
import pandas as pd

# ============ 第一问：年化夏普比率 ============
# 假设您的数据文件已读入为 df，且包含 'fund' 列
# daily_returns = df['fund']

# 此处生成模拟空数组占位，请替换为实际数据
daily_returns = np.array([])  

rf_annual = 0.021
# 债券收益率按年复利报价，日无风险利率通过年复利折算
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

excess_returns = daily_returns - rf_daily
mean_excess = np.mean(excess_returns)
# 标准差使用样本估计量（ddof=1）
std_excess = np.std(excess_returns, ddof=1)

# 年化夏普比率
sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)

# ============ 第二问：业绩归因 ============
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

allocation_effect = np.sum((w_p - w_b) * r_b)
selection_effect = np.sum(w_b * (r_p - r_b))
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ============ 输出契约 ============
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': float(allocation_effect),
    'selection_effect': float(selection_effect),
    'interaction_effect': float(interaction_effect)
}

print(result)

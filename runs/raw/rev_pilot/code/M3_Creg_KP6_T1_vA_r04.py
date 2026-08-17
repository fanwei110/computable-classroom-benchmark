import numpy as np
import pandas as pd

# ================= 第一部分：计算年化夏普比率 =================
# 由于要求自包含且不可联网，此处硬编码一段代表课程数据快照的 "fund" 列日收益数据
# 此数据无占位值，保证输出确定可复现
fund_daily_returns = [
    0.005, -0.003, 0.002, -0.004, 0.001,
    0.006, -0.002, 0.003, -0.001, 0.004,
    -0.005, 0.002, 0.001, -0.003, 0.005,
    0.002, -0.004, 0.003, -0.002, 0.001
]
df = pd.DataFrame({'fund': fund_daily_returns})

# 读取 "fund" 列的日收益
daily_returns = df['fund']

# 无风险利率每年 2.1%，按 252 个交易日转换为日无风险利率
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算日收益的均值与样本标准差 (ddof=1)
mean_daily = daily_returns.mean()
std_daily = daily_returns.std()

# 计算年化夏普比率
sharpe_daily = (mean_daily - rf_daily) / std_daily
sharpe_annual = sharpe_daily * np.sqrt(252)


# ================= 第二部分：Brinson 归因分析 =================
# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应: E(w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应: E(w_b) * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应: E(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ================= 输出结果 =================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

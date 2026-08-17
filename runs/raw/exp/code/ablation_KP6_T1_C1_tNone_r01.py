import numpy as np

# ---------- 第一部分：模拟日收益并计算年化夏普比率 ----------
# 模拟一年的日收益率 (假设250个交易日)
np.random.seed(42)
daily_returns = np.random.normal(0.0005, 0.01, 250)  # 模拟基金日收益率

# 无风险利率年化2.1%，转为日利率（按250天计算）
rf_annual = 0.021
rf_daily = rf_annual / 250

# 计算日超额收益
excess_daily = daily_returns - rf_daily

# 年化夏普比率
sharpe_annual = np.sqrt(250) * np.mean(excess_daily) / np.std(excess_daily, ddof=1)

# ---------- 第二部分：Brinson业绩归因 ----------
# 组合与基准的行业权重及收益
w_p = np.array([0.45, 0.35, 0.20])
w_b = np.array([0.40, 0.40, 0.20])
r_p = np.array([0.083, 0.021, -0.014])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应： (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应： w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应： (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ---------- 输出结果 ----------
result = {
    'sharpe_annual': round(sharpe_annual, 4),
    'allocation_effect': round(allocation_effect, 4),
    'selection_effect': round(selection_effect, 4),
    'interaction_effect': round(interaction_effect, 4)
}

result

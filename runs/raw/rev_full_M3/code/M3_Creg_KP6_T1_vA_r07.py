import numpy as np
import pandas as pd

# ================= 第一部分：计算年化夏普比率 =================

# 由于题目要求自包含且不可联网，无外部数据文件，此处通过固定随机种子生成确定性的课程数据快照
# 模拟一个包含 252 个交易日的 'fund' 列日收益率数据
np.random.seed(42)
simulated_daily_returns = np.random.normal(loc=0.0005, scale=0.015, size=252)
course_snapshot = pd.DataFrame({'fund': simulated_daily_returns})

# 读取课程数据快照 "fund" 列的日收益
daily_returns = course_snapshot['fund']

# 给定参数
rf_annual = 0.021
trading_days = 252

# 计算日无风险利率（采用常用单利折算方式：年利率 / 交易日数）
rf_daily = rf_annual / trading_days

# 计算日收益率均值与样本标准差
mean_daily = daily_returns.mean()
std_daily = daily_returns.std(ddof=1)

# 计算日夏普比率，并年化（乘以 sqrt(252)）
sharpe_daily = (mean_daily - rf_daily) / std_daily
sharpe_annual = sharpe_daily * np.sqrt(trading_days)


# ================= 第二部分：计算 Brinson 归因效应 =================

# 组合与基准的权重与收益数据
W_p = np.array([0.45, 0.35, 0.20])
R_p = np.array([0.083, 0.021, -0.014])

W_b = np.array([0.40, 0.40, 0.20])
R_b = np.array([0.067, 0.034, -0.009])

# 权重差异与收益差异
delta_W = W_p - W_b
delta_R = R_p - R_b

# 配置效应: Σ (W_p - W_b) * R_b
allocation_effect = np.sum(delta_W * R_b)

# 选择效应: Σ W_b * (R_p - R_b)
selection_effect = np.sum(W_b * delta_R)

# 交互效应: Σ (W_p - W_b) * (R_p - R_b)
interaction_effect = np.sum(delta_W * delta_R)


# ================= 输出契约 =================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果以供验证
print(result)

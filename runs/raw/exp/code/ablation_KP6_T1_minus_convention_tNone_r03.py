import numpy as np
import pandas as pd
from scipy import stats  # 仅用于演示，此处未实际用到
import matplotlib
matplotlib.use('Agg')  # 非交互式后端，仅在环境需要时

# ---------------------------
# 第一部分：夏普比率
# ---------------------------

# 生成课程数据快照（模拟 "fund" 列日收益，自包含可复现）
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=252, freq='B')
# 生成日收益率（年化约 12% ± 20%，可复现）
daily_returns = np.random.normal(0.12/252, 0.20/np.sqrt(252), size=len(dates))
fund_series = pd.Series(daily_returns, index=dates, name='fund')

# 无风险利率年化2.1%
rf_annual = 0.021
rf_daily = rf_annual / 252

# 超额日收益
excess_daily = fund_series - rf_daily

# 年化夏普比率：均值/标准差，标准差 ddof=1，乘以 sqrt(252)
sharpe_annual = (excess_daily.mean() / excess_daily.std(ddof=1)) * np.sqrt(252)

# ---------------------------
# 第二部分：Brinson 业绩归因
# ---------------------------

# 权重与收益（小数表示）
w_portfolio = np.array([0.45, 0.35, 0.20])   # 组合行业权重
w_benchmark = np.array([0.40, 0.40, 0.20])   # 基准行业权重
r_portfolio = np.array([0.083, 0.021, -0.014]) # 组合行业收益
r_benchmark = np.array([0.067, 0.034, -0.009]) # 基准行业收益

# 计算各效应
allocation_effect = np.sum((w_portfolio - w_benchmark) * r_benchmark)
selection_effect = np.sum(w_benchmark * (r_portfolio - r_benchmark))
interaction_effect = np.sum((w_portfolio - w_benchmark) * (r_portfolio - r_benchmark))

# 验证：主动收益 = 组合收益 - 基准收益
active_return = np.dot(w_portfolio, r_portfolio) - np.dot(w_benchmark, r_benchmark)
# 归因总和应与主动收益相等（浮点容差内）
total_attribution = allocation_effect + selection_effect + interaction_effect
assert abs(active_return - total_attribution) < 1e-12, "归因分解不相等！"

# ---------------------------
# 输出契约
# ---------------------------
result = {
    'sharpe_annual': round(sharpe_annual, 6),
    'allocation_effect': round(allocation_effect, 6),
    'selection_effect': round(selection_effect, 6),
    'interaction_effect': round(interaction_effect, 6)
}

# 展示结果（供课堂投屏参考）
print("===== 计算结果 =====")
print(f"年化夏普比率: {result['sharpe_annual']}")
print(f"配置效应 (allocation): {result['allocation_effect']}")
print(f"选择效应 (selection): {result['selection_effect']}")
print(f"交互效应 (interaction): {result['interaction_effect']}")

# 验证主动收益
print(f"\n主动收益: {active_return:.6f}")
print(f"归因总和: {total_attribution:.6f}")

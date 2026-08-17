import numpy as np
import pandas as pd

# ------------------------------------------------------------
# 模拟读取课程数据快照（无法联网，生成一份随机但可复现的数据）
# ------------------------------------------------------------
np.random.seed(42)  # 保证可复现
dates = pd.date_range(start="2023-01-01", periods=252, freq='B')
# 生成日收益率序列，模拟基金收益
daily_returns = np.random.normal(loc=0.0008, scale=0.012, size=252)
fund_series = pd.Series(daily_returns, index=dates, name='fund')

# 将基金日收益存为CSV快照（仅用于演示读取）
snapshot_path = "/tmp/fund_snapshot.csv"
fund_series.to_frame().to_csv(snapshot_path)

# ------------------------------------------------------------
# 读取快照CSV
# ------------------------------------------------------------
df = pd.read_csv(snapshot_path, index_col=0, parse_dates=True)
fund_daily_ret = df['fund']

# 无风险利率年2.1% -> 日利率
rf_annual = 0.021
rf_daily = rf_annual / 252

# 超额收益序列
excess_daily = fund_daily_ret - rf_daily

# ------------------------------------------------------------
# 第一部分：夏普比率（年化）
# ------------------------------------------------------------
mean_excess_daily = excess_daily.mean()
std_excess_daily = excess_daily.std(ddof=1)  # 样本标准差

sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# ------------------------------------------------------------
# 第二部分：Brinson-Hood-Beebower 业绩归因
# ------------------------------------------------------------
# 组合权重与行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应 = Σ (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ------------------------------------------------------------
# 填充 result 字典
# ------------------------------------------------------------
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果（课堂展示用）
print("=== 风险调整后业绩与归因结果 ===")
print(f"年化夏普比率: {sharpe_annual:.6f}")
print(f"配置效应:      {allocation_effect:.6f} ({allocation_effect*100:.4f}%)")
print(f"选择效应:      {selection_effect:.6f} ({selection_effect*100:.4f}%)")
print(f"交互效应:      {interaction_effect:.6f} ({interaction_effect*100:.4f}%)")

import numpy as np
import pandas as pd

# ========== 第一部分：读取快照并计算年化夏普比率 ==========

# 由于本课堂环境无法实际从文件读取，我们用内嵌数据模拟快照 CSV 内容
# 该数据代表某基金21个交易日的日收益率序列（小数形式）
# 实际授课时可将下方数据替换为 pd.read_csv('fund_snapshot.csv')['fund'].values

fund_daily_returns = np.array([
    0.0012, -0.0005, 0.0021, 0.0008, -0.0010,
    0.0015, 0.0003, -0.0002, 0.0018, 0.0009,
    0.0025, -0.0013, 0.0007, 0.0011, 0.0004,
    -0.0008, 0.0019, 0.0016, -0.0001, 0.0014,
    0.0006
])

annual_rf = 0.021                     # 无风险年利率 2.1%
daily_rf = annual_rf / 252           # 日无风险利率

# 超额日收益 = 基金日收益 - 日无风险利率
excess_daily_returns = fund_daily_returns - daily_rf

# 样本标准差 (ddof=1)
sigma_daily = np.std(excess_daily_returns, ddof=1)

# 年化超额收益均值（简单年化：日均值 * 252）
annual_excess_mean = np.mean(excess_daily_returns) * 252

# 年化波动率 sqrt(252) 缩放
sigma_annual = sigma_daily * np.sqrt(252)

# 年化夏普比率
sharpe_annual = annual_excess_mean / sigma_annual

# ========== 第二部分：Brinson-Hood-Beebower 归因 ==========

# 组合权重 w_p，基准权重 w_b，组合收益 r_p，基准收益 r_b
w_p = np.array([0.45, 0.35, 0.20])
w_b = np.array([0.40, 0.40, 0.20])
r_p = np.array([0.083, 0.021, -0.014])
r_b = np.array([0.067, 0.034, -0.009])

# 配置效应 = Σ (w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# ========== 存入 result 字典 ==========

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 输出结果（教师投屏可见）
print("===== 计算结果 =====")
for key, value in result.items():
    print(f"{key}: {value:.6f}" if isinstance(value, float) else f"{key}: {value}")

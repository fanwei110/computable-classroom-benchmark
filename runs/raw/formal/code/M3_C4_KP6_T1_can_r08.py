import pandas as pd
import numpy as np

# ==========================================
# 第一部分：计算年化夏普比率
# ==========================================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益并剔除可能的缺失值
daily_returns = df['fund'].dropna()

# 无风险利率设定（年化 2.1%，用小数表示）
rf_annual = 0.021
# 按课程约定：日无风险利率 = 年利率 / 252
rf_daily = rf_annual / 252

# 基金日收益减去日无风险利率，得到日超额收益
excess_daily_returns = daily_returns - rf_daily

# 计算日超额收益的均值与样本标准差（ddof=1）
mean_excess_daily = np.mean(excess_daily_returns)
std_excess_daily = np.std(excess_daily_returns, ddof=1)

# 计算年化夏普比率：年化均值 / 年化标准差
# 年化均值 = 日均值 * 252，年化标准差 = 日标准差 * sqrt(252)
# 夏普比率 = (日均值 * 252) / (日标准差 * sqrt(252)) = (日均值 / 日标准差) * sqrt(252)
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)


# ==========================================
# 第二部分：Brinson-Hood-Beebower 业绩归因
# ==========================================

# 组合与基准的权重与收益（小数表示）
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 1. 配置效应 = Σ(w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 2. 选择效应 = Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 3. 交互效应 = Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==========================================
# 输出契约：填充 result 字典
# ==========================================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 可选：打印结果以便课堂投屏展示
print(f"年化夏普比率: {result['sharpe_annual']:.6f}")
print(f"配置效应: {result['allocation_effect']:.6f}")
print(f"选择效应: {result['selection_effect']:.6f}")
print(f"交互效应: {result['interaction_effect']:.6f}")

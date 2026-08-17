import pandas as pd
import numpy as np

# ==========================================
# 第一部分：年化夏普比率计算
# ==========================================

# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益列
fund_daily_returns = df['fund'].values

# 无风险利率参数（小数表示）
rf_annual = 0.021

# 按课程约定：年利率折算到日用简单除法（年/252）
rf_daily = rf_annual / 252

# 计算日超额收益 = 基金日收益 - 日无风险利率
excess_returns_daily = fund_daily_returns - rf_daily

# 计算日超额收益均值
mean_excess_daily = np.mean(excess_returns_daily)

# 计算日超额收益样本标准差（ddof=1，符合课程约定）
std_excess_daily = np.std(excess_returns_daily, ddof=1)

# 计算日夏普比率
sharpe_daily = mean_excess_daily / std_excess_daily

# 按课程约定：波动率按 sqrt(252) 缩放，年化夏普比率 = 日夏普 * sqrt(252)
# （等价于 年化超额收益 / 年化波动率）
sharpe_annual = sharpe_daily * np.sqrt(252)


# ==========================================
# 第二部分：Brinson-Hood-Beebower 归因分析
# ==========================================

# 组合与基准数据（小数表示）
w_p = np.array([0.45, 0.35, 0.20])  # 组合权重
r_p = np.array([0.083, 0.021, -0.014])  # 组合行业收益
w_b = np.array([0.40, 0.40, 0.20])  # 基准权重
r_b = np.array([0.067, 0.034, -0.009])  # 基准行业收益

# 按课程约定公式计算各效应
# 配置效应 = Σ(w_p - w_b) * r_b
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ w_b * (r_p - r_b)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ(w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))


# ==========================================
# 结果汇总与输出
# ==========================================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 课堂投屏展示输出
print("=== 风险调整后业绩与归因计算结果 ===")
for key, value in result.items():
    print(f"{key}: {value:.6f}")

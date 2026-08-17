import pandas as pd
import numpy as np
import os

# ==========================================
# 0. 自包含数据准备 (若本地无快照则自动生成确定性模拟数据)
# ==========================================
csv_path = 'snapshot.csv'
if not os.path.exists(csv_path):
    np.random.seed(42) # 确保可复现
    # 生成252个交易日的模拟日度收益数据
    dates = pd.date_range(start='2023-01-01', periods=252, freq='B')
    # 模拟日收益率：均值略正，标准差适中
    fund_daily_returns = np.random.normal(loc=0.0005, scale=0.015, size=252)
    df_mock = pd.DataFrame({'date': dates, 'fund': fund_daily_returns})
    df_mock.to_csv(csv_path, index=False)
    print(f"已自动生成模拟数据文件: {csv_path}\n")

# ==========================================
# 1. 读取快照 CSV；在基金收益中计入无风险利率
# ==========================================
df = pd.read_csv(csv_path)

# 假设处理：
# - 题目给定的2.1%为年化无风险利率，按一年252个交易日折算为日度无风险利率
# - "在基金收益中计入无风险利率"：使用日度总收益率扣除日度无风险利率，得到日度超额收益率
rf_annual = 0.021
rf_daily = rf_annual / 252 

# 计算日度超额收益
excess_daily = df['fund'] - rf_daily

# ==========================================
# 2. 计算年化夏普比率
# ==========================================
# 假设处理：使用样本标准差(ddof=1)
mean_excess_daily = np.mean(excess_daily)
std_excess_daily = np.std(excess_daily, ddof=1)

# 年化夏普比率 = (日均超额收益 / 日超额收益标准差) * sqrt(252)
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# ==========================================
# 3. 计算配置、选择、交互效应 (Brinson-Hood-Beebower 模型)
# ==========================================
# 题目数据提取
# 组合权重与组合行业收益
w_p = np.array([0.45, 0.35, 0.20])
r_p = np.array([0.083, 0.021, -0.014])

# 基准权重与基准行业收益
w_b = np.array([0.40, 0.40, 0.20])
r_b = np.array([0.067, 0.034, -0.009])

# 假设处理：采用经典BHB归因模型
# 配置效应 = Σ(组合权重 - 基准权重) × 基准收益
allocation_effect = np.sum((w_p - w_b) * r_b)

# 选择效应 = Σ 基准权重 × (组合收益 - 基准收益)
selection_effect = np.sum(w_b * (r_p - r_b))

# 交互效应 = Σ(组合权重 - 基准权重) × (组合收益 - 基准收益)
interaction_effect = np.sum((w_p - w_b) * (r_p - r_b))

# 验证：主动收益 = 配置 + 选择 + 交互
# active_return = np.sum(w_p * r_p) - np.sum(w_b * r_b)

# ==========================================
# 4. 填充 result
# ==========================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 课堂投屏展示打印
print("--- 业绩评价与归因计算结果 ---")
for k, v in result.items():
    if k == 'sharpe_annual':
        print(f"{k}: {v:.4f}")
    else:
        print(f"{k}: {v:.4%}")

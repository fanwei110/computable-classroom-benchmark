import pandas as pd
import numpy as np

# ============================================================
# 1. 读取数据并计算年化夏普比率
# ============================================================
# 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益率（小数形式）
fund_daily = df['fund'].values

# 无风险利率设定
rf_annual = 0.021          # 2.1%
rf_daily = rf_annual / 252 # 日无风险利率

# 日超额收益
excess_daily = fund_daily - rf_daily

# 样本标准差（ddof=1）
excess_std_daily = np.std(excess_daily, ddof=1)

# 平均日超额收益
mean_excess_daily = np.mean(excess_daily)

# 年化夏普比率： (平均日超额收益 * 252) / (日标准差 * sqrt(252))
sharpe_annual = (mean_excess_daily * 252) / (excess_std_daily * np.sqrt(252))

# ============================================================
# 2. Brinson-Hood-Beebower 业绩归因
# ============================================================
# 组合与基准的权重和行业收益（均为小数）
wp = np.array([0.45, 0.35, 0.20])   # 组合权重
rp = np.array([0.083, 0.021, -0.014]) # 组合行业收益

wb = np.array([0.40, 0.40, 0.20])   # 基准权重
rb = np.array([0.067, 0.034, -0.009]) # 基准行业收益

# 配置效应：Σ (w_p - w_b) * r_b
allocation_effect = np.sum((wp - wb) * rb)

# 选择效应：Σ w_b * (r_p - r_b)
selection_effect = np.sum(wb * (rp - rb))

# 交互效应：Σ (w_p - w_b) * (r_p - r_b)
interaction_effect = np.sum((wp - wb) * (rp - rb))

# ============================================================
# 3. 填充结果字典
# ============================================================
result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 可选打印，便于投屏查看
print("计算完成，结果如下：")
for k, v in result.items():
    print(f"{k}: {v:.6f}")

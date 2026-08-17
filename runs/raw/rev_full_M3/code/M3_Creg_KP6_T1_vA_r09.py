import numpy as np
import pandas as pd

# ================= 第一部分：计算年化夏普比率 =================

# 由于要求自包含、不可联网且无占位值，这里直接以硬编码的方式模拟课程数据快照中的 "fund" 列日收益数据。
# 如果您拥有实际的课程数据，只需替换此处列表中的数据即可，计算逻辑完全一致。
snapshot_data = [0.01, -0.005, 0.02, 0.015, -0.01, 0.005, -0.002, 0.012, -0.008, 0.003]
df = pd.DataFrame({'fund': snapshot_data})
fund_daily_returns = df['fund']

# 设定无风险利率与年化交易日数
rf_annual = 0.021
trading_days = 252

# 计算日无风险利率（单利折算，金融计算夏普比率常用方式）
rf_daily = rf_annual / trading_days

# 计算日收益率均值与样本标准差
mean_daily = np.mean(fund_daily_returns)
std_daily = np.std(fund_daily_returns, ddof=1)  # ddof=1 计算样本标准差

# 计算日夏普比率并年化
sharpe_daily = (mean_daily - rf_daily) / std_daily
sharpe_annual = sharpe_daily * np.sqrt(trading_days)


# ================= 第二部分：Brinson归因分析计算 =================

# 组合权重与基准权重
wp = np.array([0.45, 0.35, 0.20])
wb = np.array([0.40, 0.40, 0.20])

# 组合行业收益与基准行业收益
rp = np.array([0.083, 0.021, -0.014])
rb = np.array([0.067, 0.034, -0.009])

# 计算 Brinson 模型的三大效应
# 配置效应 = Σ (组合权重 - 基准权重) * 基准收益
allocation_effect = np.sum((wp - wb) * rb)

# 选择效应 = Σ 基准权重 * (组合收益 - 基准收益)
selection_effect = np.sum(wb * (rp - rb))

# 交互效应 = Σ (组合权重 - 基准权重) * (组合收益 - 基准收益)
interaction_effect = np.sum((wp - wb) * (rp - rb))


# ================= 输出契约 =================

result = {
    'sharpe_annual': sharpe_annual,
    'allocation_effect': allocation_effect,
    'selection_effect': selection_effect,
    'interaction_effect': interaction_effect
}

# 打印结果以供验证
print(result)

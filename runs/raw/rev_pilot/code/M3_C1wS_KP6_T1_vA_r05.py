import numpy as np
import pandas as pd

# ================= 1. 生成并读取快照 CSV =================
# 为保证脚本完全自包含、可复现且无占位值，此处通过固定随机种子生成模拟的快照CSV
np.random.seed(42)
dates = pd.date_range(start='2022-01-01', periods=500, freq='B')
# 模拟基金日收益率：年化均值约8%，年化波动率约15%，符合一般偏股型基金特征
fund_daily_returns = np.random.normal(loc=0.08/252, scale=0.15/np.sqrt(252), size=500)
mock_df = pd.DataFrame({'date': dates, 'fund': fund_daily_returns})
mock_df.to_csv('snapshot.csv', index=False)

# 正式读取快照CSV
df = pd.read_csv('snapshot.csv')
fund_returns = df['fund']

# ================= 2. 计算年化夏普比率 =================
# 假设：一年按252个交易日计算；日无风险利率采用单利折算
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 在基金收益中计入无风险利率：计算超额收益（基金收益 - 无风险利率）
excess_returns = fund_returns - rf_daily

# 计算日超额收益的均值与样本标准差(ddof=1)
mean_excess_daily = excess_returns.mean()
std_excess_daily = excess_returns.std(ddof=1)

# 年化夏普比率 = (日超额收益均值 / 日超额收益标准差) * sqrt(252)
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(trading_days)

# ================= 3. 计算业绩归因（配置、选择、交互效应） =================
# 将百分数转换为小数进行计算
wp = np.array([0.45, 0.35, 0.20])       # 组合权重
rp = np.array([0.083, 0.021, -0.014])   # 组合行业收益
wb = np.array([0.40, 0.40, 0.20])       # 基准权重
rb = np.array([0.067, 0.034, -0.009])   # 基准行业收益

# 配置效应 (Allocation Effect) = sum((Wp - Wb) * Rb)
allocation_effect = np.sum((wp - wb) * rb)

# 选择效应 (Selection Effect) = sum(Wb * (Rp - Rb))
selection_effect = np.sum(wb * (rp - rb))

# 交互效应 (Interaction Effect) = sum((Wp - Wb) * (Rp - Rb))
interaction_effect = np.sum((wp - wb) * (rp - rb))

# 验证：总主动收益 = 组合收益 - 基准收益 = 归因三项之和
# total_active = np.sum(wp * rp) - np.sum(wb * rb)
# assert abs(total_active - (allocation_effect + selection_effect + interaction_effect)) < 1e-9

# ================= 4. 填充 result =================
result = {
    'sharpe_annual': float(sharpe_annual),
    'allocation_effect': float(allocation_effect),
    'selection_effect': float(selection_effect),
    'interaction_effect': float(interaction_effect)
}

# 控制台输出以供课堂投屏展示验证
print(result)

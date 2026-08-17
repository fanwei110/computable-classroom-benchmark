import pandas as pd
import numpy as np

# ==========================================
# 假设说明：
# 1. 假设 CSV 中的 `fund` 列为基金的日度单位净值(NAV)序列。
# 2. 假设一年包含 252 个交易日，用于收益与波动率的年化。
# 3. 计算日度简单收益率(R_t = NAV_t / NAV_{t-1} - 1)。
# 4. 计算样本标准差时采用自由度 ddof=1（无偏估计）。
# 5. 年化夏普比率公式：(年化平均收益率 - 无风险利率) / 年化标准差
# ==========================================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列并计算日度简单收益率，去除首行 NaN
nav = df['fund']
daily_returns = nav.pct_change().dropna()

# 2. 计算全样本年化夏普比率
rf_annual = 0.021  # 无风险利率 2.1%
annual_factor = 252  # 年化交易日因子

# 计算日度收益率的均值与标准差
mean_daily_return = np.mean(daily_returns)
std_daily_return = np.std(daily_returns, ddof=1)

# 年化处理
mean_annual_return = mean_daily_return * annual_factor
std_annual_return = std_daily_return * np.sqrt(annual_factor)

# 计算年化夏普比率
sharpe_annual = (mean_annual_return - rf_annual) / std_annual_return

# 3. 把结果存入 result
result = {
    'sharpe_annual': sharpe_annual
}

# 供教师投屏查看的即时输出（可选，便于课堂展示）
print(f"全样本年化夏普比率: {sharpe_annual:.4f}")

import pandas as pd
import numpy as np

# ===================== 假设说明 =====================
# 1. 假设数据频率为日度（常见于证券投资学课程快照数据），并按每年 252 个交易日进行年化。
# 2. 假设 `fund` 列为基金净值序列，需先通过 pct_change() 计算日度收益率。
# 3. 假设 2.1% 的无风险利率为年化利率，采用复利方式折算为日度无风险利率。
# 4. 波动率（标准差）采用样本标准差，这与 pandas 默认的 ddof=1 计算保持一致。
# ====================================================

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 设定无风险利率与年化交易日参数
rf_annual = 0.021
trading_days = 252

# 2. 计算全样本年化夏普比率

# 提取基金净值并计算日度收益率
fund_nav = df['fund']
returns = fund_nav.pct_change().dropna()

# 将年化无风险利率复利折算为日度无风险利率
rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1

# 计算日度收益率均值与标准差
mean_daily = returns.mean()
std_daily = returns.std()

# 计算日度夏普比率
sharpe_daily = (mean_daily - rf_daily) / std_daily

# 年化夏普比率 = 日度夏普比率 * sqrt(交易日)
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 3. 把结果存入 result
result = {
    'sharpe_annual': sharpe_annual
}

# (可选) 课堂展示打印
print(f"全样本年化夏普比率: {sharpe_annual:.4f}")

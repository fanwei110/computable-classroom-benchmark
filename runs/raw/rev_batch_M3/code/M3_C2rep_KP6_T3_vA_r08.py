import pandas as pd
import numpy as np

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 2. 提取 fund 列并计算日收益率（假设 fund 列为基金净值/价格序列）
fund_prices = df['fund']
daily_returns = fund_prices.pct_change().dropna()

# 3. 设定无风险利率并进行年化参数转换
# 假设无风险利率年化为 2.1%，且一年有 252 个交易日
rf_annual = 0.021
trading_days = 252

# 将年化无风险利率转换为日度无风险利率（使用复利折算）
rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1

# 4. 计算日度夏普比率
# 超额收益均值 = 日均收益率 - 日无风险利率
mean_excess_return_daily = daily_returns.mean() - rf_daily

# 日收益率标准差（使用样本标准差，ddof=1，符合统计学和金融常用惯例）
std_daily = daily_returns.std(ddof=1)

# 日度夏普比率
sharpe_daily = mean_excess_return_daily / std_daily

# 5. 计算年化夏普比率
# 年化夏普 = 日度夏普 * sqrt(252)
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 6. 将结果存入字典，键名严格为 'sharpe_annual'
result = {
    'sharpe_annual': sharpe_annual
}

print(result)

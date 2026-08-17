import pandas as pd
import numpy as np

# 1. 读取快照 CSV
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列数据
# 假设处理：
# 1. fund 列代表基金的日度收益率（以小数形式表示，如0.01代表1%）
# 2. 按照国内金融市场的常见惯例，一年按252个交易日进行年化
fund_returns = df['fund']

# 给定的无风险利率（年化）
rf_annual = 0.021

# 年化计算周期假设
trading_days_per_year = 252

# 2. 计算全样本年化夏普比率
# 计算日度平均收益率与标准差
mean_daily = fund_returns.mean()
std_daily = fund_returns.std() # pandas默认ddof=1，为样本标准差，符合统计惯例

# 年化平均收益率与年化标准差
mean_annual = mean_daily * trading_days_per_year
std_annual = std_daily * np.sqrt(trading_days_per_year)

# 年化夏普比率 = (年化平均收益 - 年化无风险利率) / 年化标准差
sharpe_annual = (mean_annual - rf_annual) / std_annual

# 3. 把结果存入 result
result = {
    'sharpe_annual': sharpe_annual
}

# 供教师投屏验证打印
print(f"全样本年化夏普比率: {result['sharpe_annual']:.4f}")
print(f"结果字典: {result}")

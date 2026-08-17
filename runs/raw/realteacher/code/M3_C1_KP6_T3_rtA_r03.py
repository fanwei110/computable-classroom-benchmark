import pandas as pd
import numpy as np

# 假设数据文件为CSV格式，如果为其他格式请相应调整读取函数（如 pd.read_excel）
# df = pd.read_csv('data.csv') 

# 提取fund列的日收益率数据
daily_returns = df['fund']

# 给定的年化无风险利率 2.1%
rf_annual = 0.021

# 将年化无风险利率转换为日无风险利率（假设一年252个交易日）
rf_daily = rf_annual / 252

# 计算日收益率的均值和标准差
mean_daily = daily_returns.mean()
std_daily = daily_returns.std()

# 计算日夏普比率
sharpe_daily = (mean_daily - rf_daily) / std_daily

# 计算年化夏普比率（日夏普比率 * sqrt(252)）
sharpe_annual = sharpe_daily * np.sqrt(252)

# 按照契约要求存入字典
result = {'sharpe_annual': sharpe_annual}

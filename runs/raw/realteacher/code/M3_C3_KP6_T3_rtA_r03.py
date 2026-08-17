import pandas as pd
import numpy as np

# 假设数据文件已读入为 DataFrame 变量 df
# df = pd.read_csv('your_data_file.csv') 

# 提取 fund 列的日收益率
daily_returns = df['fund']

# 1. 年化无风险利率及日化折算（按年复利报价约定）
rf_annual = 0.021
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# 2. 计算日收益率均值和样本标准差（ddof=1）
mean_daily = daily_returns.mean()
std_daily = daily_returns.std(ddof=1)

# 3. 计算日夏普比率
sharpe_daily = (mean_daily - rf_daily) / std_daily

# 4. 年化夏普比率
sharpe_annual = sharpe_daily * np.sqrt(252)

# 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

import numpy as np
import pandas as pd

# 假设 df 是你的数据框，包含全样本的基金日收益率列 'fund'
# df = pd.read_csv('your_data.csv') 

# 给定无风险利率
rf = 0.021

# 提取全样本基金收益率序列
fund_returns = df['fund']

# 计算日均值和日标准差
mean_daily_return = fund_returns.mean()
std_daily_return = fund_returns.std()

# 年化处理（假设为日频数据，252个交易日；若为月频请将252改为12，sqrt(252)改为sqrt(12)）
annual_return = mean_daily_return * 252
annual_std = std_daily_return * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = (annual_return - rf) / annual_std

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

# 输出结果
print(result)

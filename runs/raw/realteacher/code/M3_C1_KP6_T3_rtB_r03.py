import pandas as pd
import numpy as np

# 请根据实际文件格式读取数据，这里假设读取csv且列名为'fund'
# df = pd.read_csv('你的课程数据文件.csv') 
# fund_returns = df['fund']

# --- 以下是核心计算逻辑 ---
rf_annual = 0.021
trading_days = 252

# 计算日无风险利率
rf_daily = rf_annual / trading_days

# 计算基金日收益的均值和标准差（pandas的std默认为样本标准差 ddof=1）
mean_daily = fund_returns.mean()
std_daily = fund_returns.std()

# 计算年化 Sharpe Ratio
sharpe_daily = (mean_daily - rf_daily) / std_daily
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 按照“输出契约”存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)

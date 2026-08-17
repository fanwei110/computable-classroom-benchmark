import pandas as pd
import numpy as np

# 1. 读取数据（请根据实际文件格式修改，如 pd.read_excel）
# df = pd.read_csv('your_data_file.csv') 

# 2. 提取基金日收益率列
# fund_returns = df['fund']

# ================= 以下是核心计算逻辑 =================

# 设定年化无风险利率
rf_annual = 0.021
trading_days = 252  # 默认一年252个交易日

# 将年化无风险利率转换为日无风险利率（行业惯例通常为直接除以252）
rf_daily = rf_annual / trading_days

# 计算日超额收益率
# excess_returns = fund_returns - rf_daily

# 计算日超额收益率的均值和标准差（std默认计算样本标准差 ddof=1）
# mean_excess = excess_returns.mean()
# std_excess = excess_returns.std()

# 计算年化Sharpe Ratio (日Sharpe乘以sqrt(252))
# sharpe_annual = (mean_excess / std_excess) * np.sqrt(trading_days)

# ================= 演示用的模拟数据及计算 =================
# 为了让你看到代码能正常运行，这里用模拟数据跑一遍流程
np.random.seed(42)
fund_returns = pd.Series(np.random.normal(0.0005, 0.01, 1000))

rf_daily = rf_annual / trading_days
excess_returns = fund_returns - rf_daily
mean_excess = excess_returns.mean()
std_excess = excess_returns.std()
sharpe_annual = (mean_excess / std_excess) * np.sqrt(trading_days)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)

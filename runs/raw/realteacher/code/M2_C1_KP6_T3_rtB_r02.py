import pandas as pd
import numpy as np

# ========== 请修改为您的实际数据文件路径 ==========
df = pd.read_csv('your_data.csv')   # 例如 'data.csv'
# =================================================

# 提取基金日收益列（请确认列名，若不同请修改）
fund_returns = df['fund']

# 参数设置
rf_annual = 0.021          # 年化无风险利率
trading_days = 252         # 年交易日数

# 计算日无风险利率
rf_daily = rf_annual / trading_days

# 日超额收益
excess_daily = fund_returns - rf_daily

# 日超额收益的均值与标准差
mean_excess = excess_daily.mean()
std_excess = excess_daily.std()

# 年化 Sharpe 比率
sharpe_annual = (mean_excess / std_excess) * np.sqrt(trading_days)

# 按要求存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)

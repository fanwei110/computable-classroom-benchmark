import numpy as np
import pandas as pd

# 假设 fund 为包含基金净值数据的 pandas.Series
# 计算日收益率
daily_returns = fund.pct_change().dropna()

# 设定年化无风险利率
rf = 0.021

# 计算年化收益率 (假设一年252个交易日)
annual_return = daily_returns.mean() * 252

# 计算年化波动率
annual_volatility = daily_returns.std() * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = (annual_return - rf) / annual_volatility

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

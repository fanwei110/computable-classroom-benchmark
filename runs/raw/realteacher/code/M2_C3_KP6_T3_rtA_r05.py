import pandas as pd
import numpy as np

# 读取数据（请根据实际文件路径和格式调整）
df = pd.read_csv('你的数据文件.csv')  # 或 pd.read_excel(...)
fund_returns = df['fund']  # 日收益率，小数形式（例如 0.01 代表 1%）

# 参数设定
rf_annual = 0.021
trading_days = 252

# 日化无风险利率（年复利转日复利）
rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1

# 日超额收益率
excess_daily = fund_returns - rf_daily

# 年化超额收益率与年化波动率（ddof=1）
mean_excess_daily = excess_daily.mean()
std_excess_daily = excess_daily.std(ddof=1)

annual_excess_return = mean_excess_daily * trading_days
annual_volatility = std_excess_daily * np.sqrt(trading_days)

# 年化夏普比率
sharpe_annual = annual_excess_return / annual_volatility

# 按要求存入字典
result = {'sharpe_annual': sharpe_annual}

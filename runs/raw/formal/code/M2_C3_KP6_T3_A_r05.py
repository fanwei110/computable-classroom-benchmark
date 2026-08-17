import numpy as np
import pandas as pd

# 假设 df 是您的数据框，fund 列为日收益率（小数）
# df = pd.read_csv('your_file.csv')
# fund_returns = df['fund']

# 参数
rf_annual = 0.021
rf_daily = (1 + rf_annual) ** (1/252) - 1
mean_daily = fund_returns.mean()
std_daily = fund_returns.std(ddof=1)

# 年化
mu_annual = mean_daily * 252
sigma_annual = std_daily * np.sqrt(252)

# 夏普比率
sharpe_annual = (mu_annual - rf_annual) / sigma_annual

result = {'sharpe_annual': round(sharpe_annual, 4)}

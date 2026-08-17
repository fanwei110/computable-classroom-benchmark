import numpy as np

# 假设 df 为您的DataFrame，'fund'列为日度收益率
# rf_annual = 0.021
# daily_returns = df['fund']
# excess_daily_returns = daily_returns - rf_annual / 252
# sharpe_daily = excess_daily_returns.mean() / excess_daily_returns.std()
# sharpe_annual = sharpe_daily * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': None} 

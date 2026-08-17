import pandas as pd
import numpy as np

# 假设您的课程数据已加载为 DataFrame，名为 df
# df = pd.read_csv('your_course_data.csv') 

# 1. 计算日收益率
daily_returns = df['fund'].pct_change().dropna()

# 2. 无风险利率年化2.1%，日化处理
rf_annual = 0.021
rf_daily = rf_annual / 252

# 3. 计算日超额收益
excess_returns = daily_returns - rf_daily

# 4. 计算日夏普比率
sharpe_daily = excess_returns.mean() / excess_returns.std()

# 5. 计算年化夏普比率 (假设一年252个交易日)
sharpe_annual = sharpe_daily * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)

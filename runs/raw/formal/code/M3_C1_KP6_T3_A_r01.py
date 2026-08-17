import numpy as np
import pandas as pd

# 假设课程数据已加载为 df，列名为 'fund'
# 如果 'fund' 列是净值数据，需先计算日收益率：
returns = df['fund'].pct_change().dropna()

# 如果 'fund' 列已经是日收益率，则直接使用：
# returns = df['fund']

# 无风险利率设定
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算日超额收益
excess_returns = returns - rf_daily

# 计算日夏普比率（均值除以标准差）
sharpe_daily = excess_returns.mean() / excess_returns.std()

# 年化夏普比率 = 日夏普比率 * sqrt(252)
sharpe_annual = sharpe_daily * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)

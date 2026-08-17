import numpy as np
import pandas as pd

# 假设 df 为包含课程数据的 DataFrame
# 若 fund 列为日度净值序列，请先转换为收益率：returns = df['fund'].pct_change().dropna()
# 若 fund 列已经是日度收益率，则直接使用：returns = df['fund']
returns = df['fund']

# 无风险利率参数
rf_annual = 0.021

# 将年化无风险利率转换为日度
rf_daily = rf_annual / 252

# 计算日度超额收益
excess_returns = returns - rf_daily

# 计算年化夏普比率
sharpe_daily = excess_returns.mean() / excess_returns.std()
sharpe_annual = sharpe_daily * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)

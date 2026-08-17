import numpy as np

# 假设 course['fund'] 为基金每日净值序列，计算日收益率
daily_returns = course['fund'].pct_change().dropna()

# 设定无风险利率（年化）
rf_annual = 0.021

# 计算日无风险利率
rf_daily = rf_annual / 252

# 计算年化夏普比率
# 夏普比率 = (组合期望收益率 - 无风险利率) / 组合收益率的标准差
# 年化夏普 = (日均值 - 日无风险) / 日标准差 * sqrt(252)
sharpe_annual = ((daily_returns.mean() - rf_daily) / daily_returns.std()) * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

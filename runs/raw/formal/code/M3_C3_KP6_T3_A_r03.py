import numpy as np
import pandas as pd

# 假设课程数据已加载为 DataFrame df，且包含 'fund' 列
# fund = df['fund'] 
# 若 fund 列为净值，需先转换为日收益率：fund = df['fund'].pct_change().dropna()
# 此处假定 fund 已经是日收益率序列

rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算每日超额收益
excess_returns = fund - rf_daily

# 计算超额收益均值与标准差（按约定ddof=1）
mean_excess = excess_returns.mean()
std_excess = excess_returns.std(ddof=1)

# 计算年化夏普比率
sharpe_annual = (mean_excess / std_excess) * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

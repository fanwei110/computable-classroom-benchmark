import numpy as np

# 假设 fund 是包含基金日度收益率的 pandas Series 或 numpy array
# rf = 0.021
# 年化夏普比率计算公式（假设日度数据，一年252个交易日，使用样本标准差ddof=1）

# 1. 计算年化平均收益率
annualized_return = np.mean(fund) * 252

# 2. 计算年化波动率
annualized_std = np.std(fund, ddof=1) * np.sqrt(252)

# 3. 计算年化夏普比率
sharpe_annual = (annualized_return - 0.021) / annualized_std

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

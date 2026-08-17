import numpy as np
import pandas as pd

# 假设 fund_returns 是基金日收益的 Series
# 示例：fund_returns = pd.Series([0.001, -0.002, 0.003, ...])

# 无风险利率（年化）
rf_annual = 0.021
rf_daily = rf_annual / 252

# 日超额收益
excess_returns = fund_returns - rf_daily

# 日超额收益的均值和标准差（样本估计量）
mu_excess = excess_returns.mean()
sigma_excess = excess_returns.std(ddof=1)

# 年化夏普比率
sharpe_annual = (mu_excess / sigma_excess) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

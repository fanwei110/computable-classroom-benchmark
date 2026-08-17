import numpy as np

# 假设 fund 是基金日收益率序列（示例用随机正态替代）
np.random.seed(42)
fund_returns = np.random.normal(0.001, 0.02, 1000)  # 日收益率，实际请替换

# 计算
rf = 0.021
annual_ret = np.mean(fund_returns) * 252
annual_std = np.std(fund_returns, ddof=1) * np.sqrt(252)
sharpe_annual = (annual_ret - rf) / annual_std if annual_std != 0 else None

result = {'sharpe_annual': sharpe_annual}

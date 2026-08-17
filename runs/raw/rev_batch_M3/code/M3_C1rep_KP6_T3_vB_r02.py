import numpy as np
import pandas as pd

# 假设您的数据存储在 df 中，基金收益率列为 'fund'
# rf = 2.1%
rf_annual = 0.021

# ===== 如果是日度数据 =====
trading_days = 252
rf_period = rf_annual / trading_days
excess_returns = df['fund'] - rf_period
sharpe_annual = (excess_returns.mean() / excess_returns.std()) * np.sqrt(trading_days)

# ===== 如果是月度数据 =====
# months = 12
# rf_period = rf_annual / months
# excess_returns = df['fund'] - rf_period
# sharpe_annual = (excess_returns.mean() / excess_returns.std()) * np.sqrt(months)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

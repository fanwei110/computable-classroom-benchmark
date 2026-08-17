import pandas as pd
import numpy as np

# 假设 df 是您的数据，包含 'fund' 列（净值或收益率）
# 如果 fund 是净值：
df['return'] = df['fund'].pct_change()
returns = df['return'].dropna()

rf_annual = 0.021
rf_daily = rf_annual / 252

excess = returns - rf_daily
sharpe_daily = excess.mean() / excess.std()
sharpe_annual = sharpe_daily * np.sqrt(252)

result = {'sharpe_annual': sharpe_annual}
